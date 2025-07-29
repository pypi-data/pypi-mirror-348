import typing

if typing.TYPE_CHECKING:
    import scrapecraft  # used only for type hinting


def dispatch_locally(
    scraper: "scrapecraft.Scraper",
    tasks: typing.Union["scrapecraft.BaseTask", list["scrapecraft.BaseTask"]],
):
    """
    This will dispatch the tasks to the downloader locally
    """
    scraper.download(tasks).run()
