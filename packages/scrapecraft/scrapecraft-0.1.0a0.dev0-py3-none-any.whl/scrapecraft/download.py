import typing
from collections.abc import Callable

from blinker import Signal
from pydantic import field_validator
from pydantic_settings import BaseSettings

from .utils import get_callable_from_str, rate_limited

if typing.TYPE_CHECKING:
    import scrapecraft  # used only for type hinting


class DownloaderSettings(BaseSettings):
    get_proxy_function: typing.Optional[Callable[..., str]] = None
    # TODO: figure out how to get typing to work for the callable input and output,
    # should be Callable[["scrapecraft.Scraper", "scrapecraft.BaseTask"], str]
    download_function: Callable[..., str] = (
        "scrapecraft.download_helpers.basic_requests_downloader"
    )
    # TODO: should be Callable[["scrapecraft.Scraper", "scrapecraft.BaseTask", str], None]
    save_function: typing.Optional[Callable[..., None]] = (
        "scrapecraft.download_helpers.default_download_save"
    )

    trigger_extract_function: Callable[..., None] = (
        "scrapecraft.download_helpers.extract_locally"
    )

    filename_template: str = "scraped_data/{scrape_id}-{task_id}.html"

    @field_validator("get_proxy_function", mode="before")
    @classmethod
    def check_get_proxy_function_class(cls, value) -> typing.Optional[Callable]:
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    @field_validator("download_function", mode="before")
    @classmethod
    def check_download_function_class(cls, value) -> Callable:
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    @field_validator("save_function", mode="before")
    @classmethod
    def check_save_function_class(cls, value) -> Callable:
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    @field_validator("trigger_extract_function", mode="before")
    @classmethod
    def check_trigger_extract_function_class(cls, value) -> Callable:
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    def get_proxy(
        self,
        scraper: "scrapecraft.Scraper",
        task: "scrapecraft.BaseTask",
    ) -> typing.Optional[str]:
        """
        Get the proxy to use for the task. This can be a string or a callable that returns a string
        """
        if self.get_proxy_function is None:
            return None

        return self.get_proxy_function(scraper, task)


class Downloader:
    signal = Signal()

    def __init__(
        self,
        scraper: "scrapecraft.Scraper",
        tasks: list["scrapecraft.BaseTask"],
        settings: DownloaderSettings = DownloaderSettings(),
    ):
        self.scraper = scraper
        self.tasks = tasks
        self.settings = settings

    def run(self) -> None:
        """
        Run the downloader.
        """

        # The rate limit will be the same for all tasks in a given run,
        # so the limit in the first task is fine
        self._rate_limited_download = rate_limited(
            self.tasks[0].downloader_data.ratelimit
        )(self._rate_limited_download)

        for task in self.tasks:
            self._rate_limited_download(task)

    def _rate_limited_download(
        self,
        task: "scrapecraft.BaseTask",
    ) -> None:
        """
        Rate limit the download of tasks.
        """
        Downloader.signal.send("pre_download", scraper=self.scraper, task=task)
        source = self.settings.download_function(self.scraper, task)

        if self.settings.save_function:
            self.settings.save_function(self.scraper, task, source)

        Downloader.signal.send("post_download", scraper=self.scraper, task=task)

        # Run the trigger extract function if one exists
        if self.settings.trigger_extract_function:
            self.settings.trigger_extract_function(self.scraper, task)
