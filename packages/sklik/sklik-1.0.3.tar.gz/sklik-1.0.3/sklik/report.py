import copy
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Tuple

import pendulum

from sklik.api import SklikApi
from sklik.object import Account
from sklik.util import SKLIK_DATE_FORMAT, SKLIK_MAX_INTERVAL


def _restriction_filter_validator(
        since: Optional[str] = None,
        until: Optional[str] = None,
        restriction_filter: Optional[Dict] = None
) -> Dict[str, Any]:
    """Validate and construct date restriction parameters for a report.

    Parses the provided `since` and `until` dates and returns a dictionary
    containing the validated date range along with any additional filtering
    criteria provided in `restriction_filter`.

    Args:
        since: Start date in 'YYYY-MM-DD' format. If not provided, defaults to
            SKLIK_MAX_INTERVAL days before today.
        until: End date in 'YYYY-MM-DD' format. If not provided, defaults to
            yesterday's date.
        restriction_filter: Additional filtering criteria as a dictionary.

    Returns:
        A dictionary with keys 'dateFrom', 'dateTo', and any keys from
        `restriction_filter`.
    """
    since = pendulum.parse(since).to_date_string() if since else None
    until = pendulum.parse(until).to_date_string() if until else None

    today = pendulum.today()

    if restriction_filter is None:
        restriction_filter = {}

    full_filter = {} if restriction_filter is None else restriction_filter.copy()
    full_filter["dateFrom"] = since or today.subtract(days=SKLIK_MAX_INTERVAL).to_date_string()
    full_filter["dateTo"] = until or today.subtract(days=1).to_date_string()

    return full_filter


def _display_option_validator(granularity: Optional[str] = None) -> Dict[str, Any]:
    """Validate and construct display options for a report.

    Args:
        granularity: Time granularity for the report (e.g., 'daily', 'weekly').
            If not provided, defaults to 'daily'.

    Returns:
        A dictionary with key 'statGranularity' set to the provided or default value.
    """

    return {"statGranularity": granularity or "daily"}


@dataclass
class ReportPage:
    """Iterator for a single page of report data.

    This class handles the pagination of report data returned by the Sklik API.
    It loads a page of data and iterates over each item, fetching new pages as needed.

    Attributes:
        service: Name of the Sklik service being called.
        args: List of arguments to be passed to the API call.
        api: An instance of SklikApi used for making API calls.
    """

    service: str
    args: List
    total_count: Optional[int] = None
    api: SklikApi = field(default_factory=SklikApi.get_default_api)

    def __post_init__(self) -> None:
        """Initialize pagination parameters and load the first page."""

        self._current_index: int = 0
        self._current_offset: int = 0
        self._current_limit: int = 5000 if self.total_count is None or self.total_count > 5000 else self.total_count

        self._items_iter = self._item_generator()

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        return self

    def __next__(self) -> Dict[str, Any]:
        """Return the next report item or raise StopIteration if exhausted."""
        return next(self._items_iter)

    def _item_generator(self) -> Iterator[Dict[str, Any]]:
        """Generator that yields report items, loading new pages as necessary."""
        while True:
            page = self.load_data(self._current_offset, self._current_limit)
            if not page:
                break
            for item in page:
                yield item
            self._current_offset += self._current_limit

    def _load_raw_data(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        """Load raw report data from the API.

        Modifies the last element of `args` to include the pagination parameters.

        Args:
            offset: The offset index to start loading data.
            limit: The maximum number of records to load.

        Returns:
            A list of dictionaries representing raw report data.
        """

        payload = copy.deepcopy(self.args)
        payload[-1]["offset"] = offset
        payload[-1]["limit"] = limit
        return self.api.call(self.service, "readReport", args=payload)["report"]

    def load_data(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        """Process and load report data for the given page.

        Transforms the raw report data into a flat structure by merging
        each stat dictionary with its parent item data.

        Args:
            offset: The offset index for pagination.
            limit: The number of records to retrieve.

        Returns:
            A list of processed report items.
        """

        report = self._load_raw_data(offset, limit)
        return [
            {**stat, **{key: value for key, value in item.items() if key != "stats"}}
            for item in report
            for stat in item.get("stats", [])
        ]


@dataclass
class Report:
    """Iterator-based interface for handling Sklik API reports.

    Provides functionality to access and iterate through paginated report data
    from the Sklik advertising platform. The class handles pagination automatically
    and formats the data into a consistent structure.

    Attributes:
        account_id: Identifier of the Sklik account.
        service: Name of the Sklik service providing the report.
        report_args: List of dictionaries with report parameters (e.g., date range,
            display options).
        display_columns: List of field names to be included in the report data.
        api: An instance of SklikApi used for API calls.

    Iterator Behavior:
        The class implements the iterator protocol, allowing for easy iteration
        over all report items. Pagination is handled automatically during iteration.

    Example:
        >>> report = Report(
        ...     account_id=123456,
        ...     report_args=[
        ...         {"dateFrom": "2024-01-01", "dateTo": "2024-01-31"},
        ...         {"statGranularity": "daily"}
        ...     ],
        ...     service="stats",
        ...     display_columns=["impressions", "clicks", "cost"]
        ... )
        >>> for item in report:
        ...     print(item["impressions"], item["clicks"])
    """

    account_id: int
    service: str
    report_args: List[Dict[str, Any]]
    display_columns: List[str]
    api: SklikApi = field(default_factory=SklikApi.get_default_api)

    def __post_init__(self) -> None:
        """Initialize the report and validate input parameters.

        Validates that `report_args` contains the required date range and display
        options, and initializes internal state for pagination.

        Raises:
            ValueError: If `report_args` is invalid or missing required keys.
        """

        # Validate that report_args is a list with at least two elements
        if not isinstance(self.report_args, list) or len(self.report_args) < 2:
            raise ValueError(
                "report_args must be a list with at least two dictionaries: one for date range and one for display options."
            )

        date_args = self.report_args[0]
        display_args = self.report_args[1]

        # Validate that date_args is a dict containing 'dateFrom' and 'dateTo'
        if not isinstance(date_args, dict):
            raise ValueError("The first element of report_args must be a dictionary with date parameters.")

        if "dateFrom" not in date_args:
            raise ValueError("Missing 'dateFrom' in report_args[0].")
        if "dateTo" not in date_args:
            raise ValueError("Missing 'dateTo' in report_args[0].")

        # Validate that display_args is a dict containing 'statGranularity'
        if not isinstance(display_args, dict):
            raise ValueError("The second element of report_args must be a dictionary with display options.")

        if "statGranularity" not in display_args:
            raise ValueError("Missing 'statGranularity' in report_args[1].")

        # Validate and parse the date values
        try:
            self._start_date = pendulum.parse(date_args["dateFrom"])
            self._current_start_date = pendulum.parse(date_args["dateFrom"])
        except Exception as e:
            raise ValueError(
                f"Invalid date format for 'dateFrom': {date_args['dateFrom']}. Expected format: YYYY-MM-DD."
            ) from e

        try:
            self._end_date = pendulum.parse(date_args["dateTo"])
        except Exception as e:
            raise ValueError(
                f"Invalid date format for 'dateTo': {date_args['dateTo']}. Expected format: YYYY-MM-DD."
            ) from e

        # Assign granularity
        self._granularity = display_args["statGranularity"]

        # Initialize the report iterator
        self._current_report_page = self.load_report()

    def __iter__(self) -> "Report":
        return self

    def __next__(self) -> Dict[str, Any]:
        """Return the next report item.

        Iterates over the current page. If the current page is exhausted, attempts
        to load the next page. Stops iteration if the date range has been fully processed.

        Returns:
            The next report item as a dictionary.

        Raises:
            StopIteration: If there are no more report items.
        """

        try:
            return next(self._current_report_page)
        except StopIteration:
            if self._current_start_date > self._end_date:
                raise StopIteration()

            self._current_report_page = iter(self.load_report())
            return next(self._current_report_page)

    def _create_report(self) -> Tuple[str, int]:
        """Create a new report via the Sklik API.

        Updates the report date range parameters, creates the report and returns
        the generated report identifier.

        Returns:
            The report ID as a string.
        """

        args = copy.deepcopy(self.report_args)
        args[0]["dateFrom"], args[0]["dateTo"] = self._update_report_dates(self._current_start_date)

        self._current_start_date = pendulum.parse(args[0]["dateTo"]).add(days=1)

        payload = [{"userId": self.account_id}, *args]
        response = self.api.call(self.service, "createReport", payload)
        return response["reportId"], response["totalCount"]

    def _update_report_dates(self, start_date: pendulum) -> Tuple[str, str]:
        """Determine the appropriate date range for the next report.

        Calculates the end date based on the maximum allowed interval or the
        overall report end date.

        Args:
            start_date: The starting date for the report segment.

        Returns:
            A tuple containing the start date and end date in string format.
        """

        if self._end_date.diff(start_date).in_days() > SKLIK_MAX_INTERVAL:
            return (
                start_date.format(SKLIK_DATE_FORMAT),
                start_date.add(days=SKLIK_MAX_INTERVAL).format(SKLIK_DATE_FORMAT)
            )
        return start_date.format(SKLIK_DATE_FORMAT), self._end_date.format(SKLIK_DATE_FORMAT)

    def load_report(self) -> ReportPage:
        """Load a new report page based on the current date range.

        Creates a new report via the Sklik API and returns a ReportPage iterator
        for accessing the report data.

        Returns:
            A ReportPage instance for iterating over the report data.
        """

        report_id, total_count = self._create_report()
        return ReportPage(
            self.service,
            args=[{"userId": self.account_id}, report_id, {"displayColumns": self.display_columns}],
            total_count=total_count,
            api=self.api
        )


def create_report(
        account: Account,
        service: str,
        fields: List[str],
        since: Optional[str] = None,
        until: Optional[str] = None,
        granularity: Optional[str] = None,
        restriction_filter: Optional[Dict] = None
) -> Report:
    """Create a new report for the specified Sklik service.

    Creates and initializes a new report based on the provided parameters,
    allowing for flexible data retrieval and filtering options.

    Args:
        account: Account object containing the account ID and API instance.
        service: Name of the Sklik service to generate the report for
            (e.g., 'campaigns', 'stats', 'ads').
        fields: List of field names to include in the report.
        since: Start date for the report data in 'YYYY-MM-DD' format.
            If not specified, a default date is used.
        until: End date for the report data in 'YYYY-MM-DD' format.
            If not specified, a default date is used.
        granularity: Time granularity for the report data
            (e.g., 'daily', 'weekly', 'monthly').
        restriction_filter: Additional filtering criteria for the report data.

    Returns:
        A Report object containing the initialized report data and metadata.

    Example:
        >>> report = create_report(
        ...     account=Account(123456),
        ...     service="campaigns",
        ...     fields=["clicks", "impressions"],
        ...     since="2024-01-01",
        ...     until="2024-01-31",
        ...     granularity="daily"
        ... )
    """

    args = [
        _restriction_filter_validator(since, until, restriction_filter),
        _display_option_validator(granularity)
    ]

    return Report(account.account_id, service=service, report_args=args, display_columns=fields, api=account.api)
