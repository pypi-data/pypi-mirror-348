import os
import typing

from smart_open import open

from .utils import build_filename_template

if typing.TYPE_CHECKING:
    import scrapecraft  # used only for type hinting


def basic_requests_downloader(
    scraper: "scrapecraft.Scraper",
    task: "scrapecraft.BaseTask",
) -> str:
    """
    This is a basic downloader that will use the requests library to download the data
    """
    import requests

    proxy = scraper.settings.downloader_settings.get_proxy(scraper, task)
    if proxy:
        proxy = {
            "http": proxy,
            "https": proxy,
        }

    response = requests.request(
        method="GET",
        url=task.url,
        params=task.url_params,
        headers=task.headers,
        cookies=task.cookies,
        proxies=proxy,
    )

    # Raise an exception if an erorr status code is returned
    response.raise_for_status()

    return response.text


def default_download_save(
    scraper: "scrapecraft.Scraper",
    task: "scrapecraft.BaseTask",
    page_source: typing.Union[str, bytes],
):
    """
    This is the default save function that will save the data to a local file
    """
    filename = build_filename_template(
        template=scraper.settings.downloader_settings.filename_template,
        template_vars=task.model_dump(),
    )
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save the file
    with open(filename, "wb") as f:
        if isinstance(page_source, str):
            f.write(page_source.encode("utf-8"))
        else:
            f.write(page_source)


def extract_locally(
    scraper: "scrapecraft.Scraper",
    tasks: typing.Union["scrapecraft.BaseTask", list["scrapecraft.BaseTask"]],
):
    """
    This will dispatch the tasks to the downloader locally
    """
    if not isinstance(tasks, list):
        tasks = [tasks]
    scraper.extract(tasks).run()
