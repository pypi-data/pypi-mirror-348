import datetime
import itertools
import typing
from collections.abc import Callable

from blinker import Signal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

from .utils import get_callable_from_str, get_rate_limit_from_settings, rate_limited

if typing.TYPE_CHECKING:
    import scrapecraft  # used only for type hinting


class DispatcherSettings(BaseSettings):
    """
    Settings for the dispatcher. This will be used to configure the dispatcher
    """

    # There are 2 ways to ratelimit the dispatcher. You can either use a time interval or a number of requests per second
    # period will be the total time to run the dispatcher in seconds
    # requests_per_second will be the number of requests to send per second
    ratelimit_type: typing.Literal["period", "requests_per_second"] = (
        "requests_per_second"
    )

    # Based on the ratelimit_type, this will be the interval to send requests to the downlaoder at
    # TODO: also support times like "2h", "30m", "5s", etc only for period
    ratelimit_rate: float = Field(1.0, gt=0)

    # The number of concurrent requests to allow (local dispatch only)
    # When running locally, the concurrent requests will be the bottleneck for the rate limit if the rate limit
    # is faster then the concurrent requests can be processed
    # TODO: this may or may not be needed. Also test out threading pools vs multiprocess pools for local runs
    concurrent_requests: int = Field(1, gt=0)

    # Number of tasks to send in each download request
    # Normally this should be 1 for best results
    # But an example is your download happens in an aws fargate task using a selenium browser and has a longer spinup time,
    # you can send multiple tasks to be downloaded with a single call
    tasks_per_request: int = Field(1, gt=0)

    # The function to use to dispatch the tasks
    # TODO: Will have a few pre-built functions to use, like local, aws sns, rabbitmq, etc. Also allow to pass your own custom one
    dispatch_function: Callable = "scrapecraft.dispatch_helpers.dispatch_locally"

    # The function to use to gather the tasks
    # TODO: figure out how to get typing to work for the callable input and output,
    # should be "Callable[["scrapecraft.Scraper"], list["scrapecraft.BaseTask"]]"
    gather_tasks_function: Callable[..., list]

    @field_validator("dispatch_function", mode="before")
    @classmethod
    def check_dispatch_function_class(cls, value):
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value

    @field_validator("gather_tasks_function", mode="before")
    @classmethod
    def check_gather_tasks_function_class(cls, value):
        if isinstance(value, str):
            value = get_callable_from_str(value)
        return value


class Dispatcher:
    """
    Entrypoint for a scraper. This will gather the data that needs to be scraped and then dispatch the data to the download task
    """

    signal = Signal()

    def __init__(
        self,
        scraper: "scrapecraft.Scraper",
        settings: DispatcherSettings,
    ):
        self.scraper = scraper
        self.settings = settings

    def run(self) -> None:
        """
        Run the dispatcher. This will gather the data that needs to be scraped and then dispatch the data to the download task
        """
        # Create a signal here that will allow a user to listen for
        # the start of the scraping process

        Dispatcher.signal.send("pre_gather", scraper=self.scraper)
        tasks = self.settings.gather_tasks_function(self.scraper)

        # Set up rate limiting based on settings
        rate_limit_rps = get_rate_limit_from_settings(self.settings)
        # If there are multiple tasks per request, we need to account for that in both the dispatch rate and the download rate
        # This way the rate limit set by the user is matches the actual download rate
        dispatch_rate_limit_rps = rate_limit_rps / self.settings.tasks_per_request
        self._rate_limited_dispatch = rate_limited(dispatch_rate_limit_rps)(
            self._rate_limited_dispatch
        )

        # Send tasks to the downloader
        for tasks in itertools.batched(tasks, self.settings.tasks_per_request):
            self._rate_limited_dispatch(tasks, rate_limit_rps)

    def _rate_limited_dispatch(
        self,
        tasks: list["scrapecraft.BaseTask"],
        rate_limit: float,
    ) -> None:
        # Update the dispatched_at timestamp for each task before sending
        for task in tasks:
            task.dispatched_at = datetime.datetime.now(datetime.timezone.utc)
            task.downloader_data.ratelimit = rate_limit

        Dispatcher.signal.send("send_task", scraper=self.scraper, tasks=tasks)
        self.settings.dispatch_function(self.scraper, tasks)
