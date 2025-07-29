import json
import os
import typing
from typing import Any, Dict, List

if typing.TYPE_CHECKING:
    from parsel import Selector

    import scrapecraft  # used only for type hinting

from .utils import build_filename_template


def prepare_html_source(source_path: str) -> "Selector":
    """
    Prepare an HTML source by reading the file and converting it to a parsel Selector.

    Args:
        source_path: Path to the HTML file to process

    Returns:
        A parsel Selector object initialized with the HTML content
    """
    from parsel import Selector

    # Read the HTML file
    with open(source_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Create a Selector object
    return Selector(text=html_content)


def extract_with_parsel(
    scraper: "scrapecraft.Scraper",
    task: "scrapecraft.BaseTask",
    selector: "Selector",
    extractor_def: "scrapecraft.ExtractorDefinition",
) -> List[Dict[str, Any]]:
    """
    Extract data from a parsel Selector using the provided extractor definition.

    Args:
        selector: The parsel Selector containing the HTML to extract from
        extractor_def: Definition of what to extract
        task: The task associated with this extraction

    Returns:
        List of extracted items
    """
    results = []

    # Handle both single selector and list of selectors
    selectors = extractor_def.selectors
    if isinstance(selectors, str):
        selectors = [selectors]

    # Try each selector until one returns elements
    elements = []
    for css_selector in selectors:
        elements = selector.css(css_selector)
        if elements:
            break

    # Process each matched element
    for element in elements:
        item = {}

        # Use custom extractor function if provided
        if extractor_def.extractor_function:
            extracted_data = extractor_def.extractor_function(scraper, task, element)
            if isinstance(extracted_data, dict):
                item.update(extracted_data)
            else:
                item["content"] = extracted_data
        else:
            # Default extraction - get text content
            item["content"] = element.get().strip()

        # Add any additional fields from the extractor definition
        if extractor_def.additional_fields:
            item.update(extractor_def.additional_fields)

        results.append(item)

    return results


def default_extract_save(
    scraper: "scrapecraft.Scraper",
    task: "scrapecraft.BaseTask",
    extracted_data: List[Dict[str, Any]],
    extractor_def: "scrapecraft.ExtractorDefinition",
    template_vars: Dict[str, Any],
) -> None:
    """
    Save extracted data to a file.

    Args:
        scraper: The scraper instance
        task: The task that was processed
        extracted_data: The data that was extracted
        extractor_def: The extractor definition used
        template_vars: Variables for the filename template
    """
    # Generate filename from template
    filename = build_filename_template(
        template=scraper.settings.extractor_settings.filename_template,
        template_vars=template_vars,
    )

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save to file (as JSON)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=2, ensure_ascii=False)
