import typing
from collections.abc import Callable
from typing import Any, Dict, List, Optional, Union

from blinker import Signal
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings

from .utils import build_filename_template, get_callable_from_str

if typing.TYPE_CHECKING:
    import scrapecraft  # used only for type hinting


class ExtractorDefinition(BaseModel):
    """
    Definition for how to extract data from a source.
    """

    # Name of this extractor for identification
    name: str

    # CSS selectors to locate elements (will try each until one returns data)
    selectors: Union[str, List[str]]

    # Optional function to extract specific data from each element
    # If not provided, will use the text content of the element
    extractor_function: Optional[Callable] = None

    # Optional fields to include with each extracted item
    additional_fields: Dict[str, Any] = {}


class ExtractorSettings(BaseSettings):
    """
    Settings for the extractor.
    """

    # Function to prepare the source (e.g., converting HTML to Selector object)
    prepare_source_function: Callable[..., Any] = (
        "scrapecraft.extract_helpers.prepare_html_source"
    )

    # Function to extract data based on extractor definitions
    extract_function: Callable[..., List[Dict[str, Any]]] = (
        "scrapecraft.extract_helpers.extract_with_parsel"
    )

    # Function to save extracted data
    save_function: Optional[Callable[..., None]] = (
        "scrapecraft.extract_helpers.default_extract_save"
    )

    # Template for output filenames
    filename_template: str = (
        "extracted_data/{scrape_id}-{task_id}-{extractor_name}.json"
    )

    # Definitions of what to extract
    extractors: List[ExtractorDefinition] = []

    @field_validator("prepare_source_function", mode="before")
    @classmethod
    def check_prepare_source_function(cls, value) -> Callable:
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    @field_validator("extract_function", mode="before")
    @classmethod
    def check_extract_function(cls, value) -> Callable:
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    @field_validator("save_function", mode="before")
    @classmethod
    def check_save_function(cls, value) -> Optional[Callable]:
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value


class Extractor:
    """
    Handles extraction of data from downloaded sources.
    """

    signal = Signal()

    def __init__(
        self,
        scraper: "scrapecraft.Scraper",
        tasks: list["scrapecraft.BaseTask"],
        settings: ExtractorSettings = ExtractorSettings(),
    ):
        self.scraper = scraper
        self.tasks = tasks
        self.settings = settings

    def run(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Run the extractor on all tasks.

        Returns:
            Dict mapping task IDs to lists of extracted items.
        """
        results = {}

        for task in self.tasks:
            task_results = self.extract_task(task)
            results[task.task_id] = task_results

        return results

    def extract_task(
        self, task: "scrapecraft.BaseTask"
    ) -> List[Dict[str, Dict[str, Any]]]:
        """
        Extract data from a single task using all defined extractors.

        Args:
            task: The task containing source data to extract from

        Returns:
            List of extracted items for each extractor
        """
        Extractor.signal.send("pre_extract", scraper=self.scraper, task=task)

        # Get the source file path from the task
        # This assumes the download module has saved the source somewhere
        # and the path is available in the task
        source_path = build_filename_template(
            template=self.scraper.settings.downloader_settings.filename_template,
            template_vars=task.model_dump(),
        )

        # Prepare the source (convert to parsel Selector if HTML)
        prepared_source = self.settings.prepare_source_function(source_path)

        # Extract data using all defined extractors
        all_results = []

        for extractor_def in self.settings.extractors:
            extracted_data = self.settings.extract_function(
                self.scraper, task, prepared_source, extractor_def
            )

            # Save extracted data if a save function is defined
            if self.settings.save_function:
                template_vars = task.model_dump()
                template_vars["extractor_name"] = extractor_def.name

                self.settings.save_function(
                    self.scraper, task, extracted_data, extractor_def, template_vars
                )

            all_results.append(
                {"extractor": extractor_def.name, "data": extracted_data}
            )

        Extractor.signal.send(
            "post_extract", scraper=self.scraper, task=task, results=all_results
        )

        return all_results
