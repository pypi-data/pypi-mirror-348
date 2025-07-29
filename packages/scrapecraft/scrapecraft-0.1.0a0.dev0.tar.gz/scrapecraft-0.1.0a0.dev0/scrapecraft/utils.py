import datetime
import re
import threading
import time
import typing
from functools import wraps
from typing import Callable, cast

from pydantic import BaseModel
from ulid import ULID

if typing.TYPE_CHECKING:
    import scrapecraft  # used only for type hinting


class DownloaderData(BaseModel):
    ratelimit: float = None


class BaseTask(BaseModel):
    """
    This is the base task. This object will get passed around to the different steps
    """

    # A Unique id that will be used to identify this scraper instance
    # This will stay the same with each re-extraction
    scrape_id: str = str(ULID())

    # A unique id for each time this scraper is run/re-run
    # This is useful to have a new run_id each time a new re-extraction is run
    run_id: str = str(ULID())

    # A unique id for each task
    # This is useful to have a new task_id each time a new task is created
    task_id: str = str(ULID())

    # The timestamp the task was created
    created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    # The timestamp of when the task was dispatched
    dispatched_at: datetime.datetime = None
    # The timestamp of when the task was downloaded
    downloaded_at: datetime.datetime = None
    # The timestamp of when the task was extracted
    extracted_at: datetime.datetime = None

    # The url to scrape
    url: str = None
    # Url params to send to the downloader
    url_params: dict = {}
    # The headers to send to the downloader
    headers: dict = {}
    # The cookies to send to the downloader
    cookies: dict = {}

    # TODO: this would also be a model that should not be allowed on init as its intended to be used by the code to pass needed info along
    downloader_data: DownloaderData = DownloaderData()

    # For the user to add any custom data to the task
    custom_data: dict = {}

    def __copy__(self):
        """
        Create a new instance of the task with the same data
        """
        # task_id should always be unique, even if copied
        self.task_id = str(ULID())
        return super().__copy__()


def rate_limit_from_period(num_ref_data, period):
    """Generate the QPS from a period (hrs)

    Args:
        num_ref_data (int): Number of lambda calls needed
        period (float): Number of hours to spread out the calls

    Returns:
        float: Queries per second
    """
    seconds = period * 60 * 60
    qps = num_ref_data / seconds
    return qps


def get_callable_from_str(
    callable_str: typing.Union[str, typing.Callable],
) -> typing.Callable:
    """Get the callable from a string

    Args:
        callable_str (str): The string to get the callable from

    Returns:
        callable: The callable

    """
    if isinstance(callable_str, str):
        # Import the module and class from the string
        module_name, class_name = callable_str.rsplit(".", 1)
        module = __import__(module_name, fromlist=[class_name])
        dispatcher_class = getattr(module, class_name)

    elif isinstance(callable_str, typing.Callable):
        # If it's already a callable
        dispatcher_class = callable_str

    else:
        raise ValueError(f"Invalid callable: {callable_str}")

    return dispatcher_class


def rate_limited[T, **P](
    max_per_second: float,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Rate limit a function to a maximum number of calls per second.
    Original Source from: https://gist.github.com/gregburek/1441055?permalink_comment_id=5186398#gistcomment-5186398
    Args:
        max_per_second (float): The maximum number of calls per second
    Returns:
        Callable[[Callable[P, T]], Callable[P, T]]: The rate limited function
    """

    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        lock = threading.RLock()
        min_interval = 1.0 / max_per_second
        last_time_called = 0.0

        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            with lock:
                nonlocal last_time_called
                elapsed = time.perf_counter() - last_time_called
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)

                last_time_called = time.perf_counter()
                return fn(*args, **kwargs)

        return cast(Callable[P, T], wrapper)

    return decorator


def get_rate_limit_from_settings(
    settings: "scrapecraft.dispatch.DispatcherSettings",
    total_task_count: int = 0,
) -> float:
    """Get the rate limit from the dispatchers settings

    Args:
        settings (scrapcraft.dispatch.DispatcherSettings): The settings to get the rate limit from
        total_task_count (int): The total number of tasks to be dispatched

    Returns:
        float: The rate limit in requests per second
    """
    if settings.ratelimit_type == "period":
        return rate_limit_from_period(total_task_count, settings.ratelimit_rate)

    elif settings.ratelimit_type == "requests_per_second":
        return settings.ratelimit_rate

    else:
        raise ValueError(f"Invalid ratelimit type: {settings.ratelimit_type}")


def build_filename_template(
    template: str,
    template_vars: dict,
):
    """
    Generate the fininal filename from the template and the task object.
    Supports both standard variable replacement {variable} and nested attributes
    using dot notation {variable.nested_attr}.
    """

    # Find all variables in the template that need to be replaced
    var_pattern = re.compile(r"{([^{}]+)}")
    vars_to_replace = var_pattern.findall(template)

    # Function to resolve a variable path (e.g., "url_params.param")
    def resolve_variable(var_path, data_dict):
        parts = var_path.split(".")
        current = data_dict

        # Navigate through the nested structure
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                # If can't resolve, return None
                return None

        return current

    print(f"template vars: {template_vars}")
    # Replace variables in the template
    filename = template
    for var in vars_to_replace:
        # Get value from task dictionary, handling nested attributes
        value = resolve_variable(var, template_vars)

        print(f"Replacing variable: {var} with value: {value}")

        if value is not None:
            # Convert the value to string if it's not already
            var_value = str(value)
            # Replace the variable in the template
            filename = filename.replace(f"{{{var}}}", var_value)

    if not filename:
        raise ValueError("Generated filename is empty after processing the template.")

    return filename
