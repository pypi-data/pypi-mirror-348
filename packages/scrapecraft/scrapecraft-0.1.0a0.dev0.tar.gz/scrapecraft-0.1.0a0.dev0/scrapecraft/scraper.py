import os
import sys

from pydantic import field_validator
from pydantic_settings import BaseSettings

from .dispatch import Dispatcher, DispatcherSettings
from .download import Downloader, DownloaderSettings
from .extract import Extractor, ExtractorSettings
from .utils import get_callable_from_str


class ScraperSettings(BaseSettings):
    """
    Settings for the scraper. This will be used to configure the scraper
    """

    # Default to the file name being run
    # This will be used to identify the scraper
    name: str = os.path.basename(sys.argv[0]).rsplit(".", 1)[0]

    # Can be either a string path to a module to import or a Dispatcher instance or subclass
    dispatcher: type["Dispatcher"] = Dispatcher
    dispatcher_settings: DispatcherSettings

    downloader: type["Downloader"] = Downloader
    downloader_settings: DownloaderSettings = DownloaderSettings()

    extractor: type["Extractor"] = Extractor
    extractor_settings: ExtractorSettings = ExtractorSettings()

    @field_validator("dispatcher", mode="before")
    @classmethod
    def check_dispatcher_class(cls, value):
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    @field_validator("downloader", mode="before")
    @classmethod
    def check_downloader_class(cls, value):
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    @field_validator("extractor", mode="before")
    @classmethod
    def check_extractor_class(cls, value):
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value


class Scraper:
    def __init__(self, settings: ScraperSettings):
        self.settings = settings

    def __str__(self):
        return f'Scraper("{self.settings.name}")'

    def dispatch(self, *args, **kwargs):
        """
        This will create a dispatcher object and return it
        """
        return self.settings.dispatcher(
            self, settings=self.settings.dispatcher_settings, *args, **kwargs
        )

    def download(self, tasks, *args, **kwargs):
        """
        This will create a downloader object and return it
        """
        return self.settings.downloader(
            self, tasks, settings=self.settings.downloader_settings, *args, **kwargs
        )

    def extract(self, task, *args, **kwargs):
        """
        This will create an extractor object and return it
        """
        return self.settings.extractor(
            self, task, settings=self.settings.extractor_settings, *args, **kwargs
        )
