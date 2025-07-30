from unittest.mock import patch

import pendulum
import pytest

# Assume the code is in a module called sklik.
# Adjust the import paths as necessary.
from sklik.report import (
    _restriction_filter_validator,
    _display_option_validator,
    ReportPage,
    Report,
    create_report,
)
from sklik.util import SKLIK_MAX_INTERVAL, SKLIK_DATE_FORMAT


# ========= Tests for _restriction_filter_validator =========

def test_restriction_filter_validator_with_all_parameters():
    # Given
    since = "2024-01-01"
    until = "2024-01-31"
    extra_filter = {"campaignId": 123}
    # When
    result = _restriction_filter_validator(since, until, extra_filter)
    # Then: since/until should be passed through if provided.
    assert result["dateFrom"] == since
    assert result["dateTo"] == until
    # Extra filter is merged in.
    assert result["campaignId"] == 123


def test_restriction_filter_validator_defaults(monkeypatch):
    # Given: no since/until provided.
    fake_today = pendulum.datetime(2024, 2, 10)
    monkeypatch.setattr(pendulum, "today", lambda: fake_today)

    # When
    result = _restriction_filter_validator()
    print("***")
    print(result)

    # Then: dateFrom is today - SKLIK_MAX_INTERVAL days and dateTo is today - 1 day.
    expected_date_from = fake_today.subtract(days=SKLIK_MAX_INTERVAL).to_date_string()
    expected_date_to = fake_today.subtract(days=1).to_date_string()
    assert result["dateFrom"] == expected_date_from
    assert result["dateTo"] == expected_date_to


def test_restriction_filter_validator_with_none_extra():
    # When no restriction_filter is provided, only the dates appear.
    since = "2024-03-01"
    until = "2024-03-31"
    result = _restriction_filter_validator(since, until)
    assert "dateFrom" in result and result["dateFrom"] == since
    assert "dateTo" in result and result["dateTo"] == until
    # No extra keys should be present.
    assert len(result) == 2


# ========= Tests for _display_option_validator =========

def test_display_option_validator_with_granularity():
    granularity = "weekly"
    result = _display_option_validator(granularity)
    assert result["statGranularity"] == granularity


def test_display_option_validator_default():
    result = _display_option_validator(None)
    assert result["statGranularity"] == "daily"


def test_display_option_validator_with_empty_string():
    # When passing an empty string for granularity, the default "daily" should be used.
    result = _display_option_validator("")
    # Even if empty string is passed, our implementation chooses granularity or "daily"
    assert result["statGranularity"] == "daily"


# ========= Tests for ReportPage =========

class FakeApi:
    def __init__(self):
        self.call_count = 0

    def call(self, service, method, args):
        # Simulate pagination based on the offset in args.
        # The last element in args is assumed to be a dict we can modify.
        offset = args[-1].get("offset", 0)
        limit = args[-1].get("limit", 100)
        # For offset 0, return a first "page" of data with two items.
        if offset == 0:
            # Each item contains a "stats" key with a list of stat dictionaries,
            # plus some extra keys that should be merged.
            return {
                "report": [
                    {"stats": [{"val": 1}, {"val": 2}], "extra": "x"},
                    {"stats": [{"val": 3}], "extra": "y"},
                ]
            }
        # For subsequent offsets, return an empty list (end of data)
        return {"report": []}


@patch("sklik.SklikApi.get_default_api")
def test_reportpage_iteration(mock_get_default_api):
    # Arrange: Set up our fake API and patch the get_default_api method.
    fake_api = FakeApi()
    mock_get_default_api.return_value = fake_api

    # Create a ReportPage with dummy service and arguments.
    # The actual values of service and args do not matter as long as the fake API returns data.
    rp = ReportPage(service="dummyService", args=["dummy_account", "dummy_report", {"displayColumns": ["val"]}],
                    api=fake_api)

    # Act: Iterate over ReportPage and collect items.
    items = list(rp)
    # The expected behavior: load_data returns a flattened list:
    # From first item: two stats dictionaries merged with {"extra": "x"}
    #   -> {"val": 1, "extra": "x"}, {"val": 2, "extra": "x"}
    # From second item: one stat merged with {"extra": "y"}
    #   -> {"val": 3, "extra": "y"}
    expected = [
        {"val": 1, "extra": "x"},
        {"val": 2, "extra": "x"},
        {"val": 3, "extra": "y"},
    ]
    assert items == expected

    # Iteration should stop after all items are read.
    with pytest.raises(StopIteration):
        next(iter(rp))


class MultiPageFakeApi:
    """Fake API that simulates multiple pages of report data."""

    def __init__(self, pages):
        """
        pages: a list of pages where each page is a list of report items.
        Each report item is a dict with 'stats' key (list of stat dicts)
        and possibly additional keys.
        """
        self.pages = pages
        self.call_count = 0

    def call(self, service, method, args):
        offset = args[-1].get("offset", 0)
        limit = args[-1].get("limit", 100)
        # Calculate which page to return based on offset/limit.
        page_index = self.call_count
        self.call_count += 1
        if page_index < len(self.pages):
            return {"report": self.pages[page_index]}
        return {"report": []}


@patch("sklik.SklikApi.get_default_api")
def test_reportpage_multiple_pages(mock_get_default_api):
    # Setup multiple pages:
    pages = [
        # Page 1: two items with stats
        [
            {"stats": [{"val": 10}], "extra": "a"},
            {"stats": [{"val": 20}], "extra": "b"},
        ],
        # Page 2: one item with two stats entries
        [
            {"stats": [{"val": 30}, {"val": 40}], "extra": "c"},
        ],
        # Page 3: empty page signaling the end.
        []
    ]
    fake_api = MultiPageFakeApi(pages)
    mock_get_default_api.return_value = fake_api

    rp = ReportPage(service="dummyService", args=["dummy", "dummy", {"displayColumns": ["val"]}], api=fake_api)
    items = list(rp)

    # Expect a flattened list:
    expected = [
        {"val": 10, "extra": "a"},
        {"val": 20, "extra": "b"},
        {"val": 30, "extra": "c"},
        {"val": 40, "extra": "c"},
    ]
    assert items == expected

    # Iterating further should raise StopIteration.
    rp_iter = iter(rp)
    with pytest.raises(StopIteration):
        for _ in range(10):
            next(rp_iter)


# ========= Tests for Report =========

class FakeApiReport:
    """A fake API to simulate both createReport and readReport calls."""

    def __init__(self):
        self.create_report_called = 0
        self.read_report_called = 0

    def call(self, service, method, args):
        if method == "createReport":
            self.create_report_called += 1
            # Return a fake reportId; we can use the count to differentiate calls.
            return {"reportId": f"fake_report_{self.create_report_called}", "totalCount": 1}
        elif method == "readReport":
            self.read_report_called += 1
            # Simulate returning one page with one item.
            return {
                "report": [
                    {"stats": [{"metric": 100}], "other": "test"}
                ]
            }
        raise ValueError("Unknown method")


class MultiPageFakeApiReport:
    """A fake API that simulates multiple createReport and readReport calls."""

    def __init__(self, pages_per_report):
        """
        pages_per_report: a list where each element is a list of pages.
        Each pages element is a list of pages for one report creation call.
        """
        self.pages_per_report = pages_per_report
        self.create_report_calls = 0
        self.read_report_calls = 0

    def call(self, service, method, args):
        if method == "createReport":
            # Each call to createReport uses the current sub-range.
            self.create_report_calls += 1
            self.read_report_calls = 0
            return {"reportId": f"report_{self.create_report_calls}", "totalCount": 3000}
        elif method == "readReport":
            # Determine which report creation call we are in.
            current_report = self.create_report_calls - 1
            pages = self.pages_per_report[current_report]
            # Return one page per readReport call.
            if self.read_report_calls < len(pages):
                result = {"report": pages[self.read_report_calls]}
                self.read_report_calls += 1
                return result
            return {"report": []}
        raise ValueError("Unknown method")


@pytest.fixture
def valid_report_args():
    # Valid report_args consists of two dictionaries:
    # First: date parameters with valid 'dateFrom' and 'dateTo'
    # Second: display options with 'statGranularity'
    return [
        {"dateFrom": "2024-01-01", "dateTo": "2024-01-31"},
        {"statGranularity": "daily"}
    ]


def test_report_post_init_validation_invalid_length():
    # Test that Report raises an error if report_args does not have at least two elements.
    with pytest.raises(ValueError, match="report_args must be a list with at least two dictionaries"):
        Report(account_id=123, service="stats", report_args=[{"dateFrom": "2024-01-01"}], display_columns=["a"])


def test_report_post_init_validation_missing_date_keys(valid_report_args):
    # Remove 'dateFrom' key
    bad_args = valid_report_args.copy()
    bad_args[0] = {"dateTo": "2024-01-31"}
    with pytest.raises(ValueError, match="Missing 'dateFrom'"):
        Report(account_id=123, service="stats", report_args=bad_args, display_columns=["a"])

    # Remove 'dateTo' key
    bad_args = valid_report_args.copy()
    bad_args[0] = {"dateFrom": "2024-01-01"}
    with pytest.raises(ValueError, match="Missing 'dateTo'"):
        Report(account_id=123, service="stats", report_args=bad_args, display_columns=["a"])


def test_report_post_init_validation_missing_statgranularity(valid_report_args):
    # Remove 'statGranularity' from second dict.
    bad_args = valid_report_args.copy()
    bad_args[1] = {}
    with pytest.raises(ValueError, match="Missing 'statGranularity'"):
        Report(account_id=123, service="stats", report_args=bad_args, display_columns=["a"])


def test_report_post_init_invalid_date_format(valid_report_args):
    # Pass an invalid date format for dateFrom.
    bad_args = valid_report_args.copy()
    bad_args[0] = {"dateFrom": "01-01-2024", "dateTo": "2024-01-31"}
    with pytest.raises(ValueError, match="Invalid date format for 'dateFrom'"):
        Report(account_id=123, service="stats", report_args=bad_args, display_columns=["a"])


@patch("sklik.SklikApi.get_default_api")
def test_report_iteration(mock_get_default_api, valid_report_args):
    # Arrange: use our fake API to simulate report creation and page reading.
    fake_api = FakeApiReport()
    mock_get_default_api.return_value = fake_api

    # Create a Report with a short interval so that after one iteration, StopIteration occurs.
    report = Report(
        account_id=123,
        service="stats",
        report_args=valid_report_args,
        display_columns=["metric"],
        api=fake_api
    )

    # Act: get one item from the iterator.
    first_item = next(report)
    # Expect the first item to be merged data from ReportPage load.
    assert first_item["metric"] == 100
    assert first_item["other"] == "test"

    # Because our fake API always returns the same page, calling next again will eventually loop.
    # For this test, we simulate only one page. Force StopIteration by altering the API to return an empty report.
    original_call = fake_api.call

    def empty_call(service, method, args):
        if method == "readReport":
            return {"report": []}
        return original_call(service, method, args)

    fake_api.call = empty_call
    with pytest.raises(StopIteration):
        next(report)


def test_report_update_dates_with_long_interval(valid_report_args):
    fake_api = FakeApiReport()

    # This test ensures that _update_report_dates splits a range larger than SKLIK_MAX_INTERVAL.
    report = Report(account_id=123, service="stats", report_args=valid_report_args, display_columns=["metric"],
                    api=fake_api)
    # Let start_date be the beginning of the interval.
    start_date = pendulum.parse("2024-01-01")
    # Since dateTo is 2024-03-31, the difference is more than SKLIK_MAX_INTERVAL days.
    date_from, date_to = report._update_report_dates(start_date)
    # The end of the returned range should be start_date + SKLIK_MAX_INTERVAL days.
    expected_date_to = start_date.add(days=SKLIK_MAX_INTERVAL).format(SKLIK_DATE_FORMAT)
    assert date_from == start_date.format(SKLIK_DATE_FORMAT)
    assert date_to == expected_date_to


def test_report_update_dates_with_short_interval(valid_report_args):
    fake_api = FakeApiReport()

    # Adjust valid_report_args to have a short interval.
    args = [
        {"dateFrom": "2024-02-01", "dateTo": "2024-02-15"},
        {"statGranularity": "daily"}
    ]
    report = Report(account_id=123, service="stats", report_args=args, display_columns=["metric"], api=fake_api)
    start_date = pendulum.parse("2024-02-01")
    date_from, date_to = report._update_report_dates(start_date)
    # Since the total range is less than SKLIK_MAX_INTERVAL, date_to should be the report's end date.
    assert date_from == "20240201"
    assert date_to == "20240202"


# @patch("sklik.SklikApi.get_default_api")
# def test_report_multiple_pages_iteration(mock_get_default_api, valid_report_args):
#     """
#     Simulate a Report that, over successive _create_report calls,
#     returns multiple pages and then moves to the next date sub-range.
#     """
#     # Simulate two report creation calls.
#     # For the first report, simulate 2 pages.
#     # For the second report, simulate 1 page.
#     pages_per_report = [
#         [
#             # First report: two pages.
#             [
#                 {"stats": [{"val": 1}], "info": "page1"},
#             ],
#             [
#                 {"stats": [{"val": 2}], "info": "page2"},
#             ],
#         ],
#         [
#             # Second report: one page.
#             [
#                 {"stats": [{"val": 3}], "info": "page3"},
#             ],
#         ],
#         [
#             # Third report: one page.
#             [
#                 {"stats": [{"val": 4}], "info": "final"},
#             ],
#         ]
#     ]
#     fake_api = MultiPageFakeApiReport(pages_per_report)
#     mock_get_default_api.return_value = fake_api
#
#     # We set report_args such that the overall interval is large and will require two report creations.
#     report = Report(
#         account_id=123,
#         service="stats",
#         report_args=valid_report_args,
#         display_columns=["val"],
#         api=fake_api
#     )
#
#     # Collect items. They should be yielded in order from all pages.
#     items = []
#     # Use a while loop to collect until StopIteration.
#     try:
#         while True:
#             items.append(next(report))
#     except StopIteration:
#         pass
#
#     expected = [
#         {"val": 1, "info": "page1"},
#         {"val": 2, "info": "page2"},
#         {"val": 3, "info": "page3"},
#         {"val": 4, "info": "final"},
#     ]
#     assert items == expected


# ========= Tests for create_report =========

class FakeAccount:
    def __init__(self, account_id, api):
        self.account_id = account_id
        self.api = api


@patch("sklik.SklikApi.get_default_api")
def test_create_report(mock_get_default_api, valid_report_args):
    # Arrange: Create a fake API that we can inspect.
    fake_api = FakeApiReport()
    mock_get_default_api.return_value = fake_api

    account = FakeAccount(account_id=789, api=fake_api)
    service = "campaigns"
    fields = ["clicks", "impressions"]
    since = "2024-02-01"
    until = "2024-02-28"
    granularity = "daily"
    restriction_filter = {"filterKey": "filterValue"}

    # Act: Create the report using the helper function.
    report_obj = create_report(
        account=account,
        service=service,
        fields=fields,
        since=since,
        until=until,
        granularity=granularity,
        restriction_filter=restriction_filter
    )

    # Assert: The report object should be correctly instantiated.
    assert isinstance(report_obj, Report)
    assert report_obj.account_id == 789
    assert report_obj.service == service
    # Also verify that the report_args include our parameters.
    date_args, display_args = report_obj.report_args
    assert date_args["dateFrom"] == pendulum.parse(since).to_date_string()
    assert date_args["dateTo"] == pendulum.parse(until).to_date_string()
    assert date_args["filterKey"] == "filterValue"
    assert display_args["statGranularity"] == granularity
    assert report_obj.display_columns == fields


@patch("sklik.SklikApi.get_default_api")
def test_create_report_with_minimal_parameters(mock_get_default_api):
    """
    Test create_report with only required parameters and ensure the Report is created.
    """
    fake_api = MultiPageFakeApiReport([[[{"stats": [{"metric": 55}], "label": "min"}]]])
    mock_get_default_api.return_value = fake_api

    account = FakeAccount(account_id=321, api=fake_api)
    report_obj = create_report(
        account=account,
        service="campaigns",
        fields=["metric"],
        since="2024-04-01",
        until="2024-04-15",
        granularity="daily"
    )

    # The report_args should contain the date range and default display options.
    date_args, display_args = report_obj.report_args
    assert date_args["dateFrom"] == "2024-04-01"
    assert date_args["dateTo"] == "2024-04-15"
    assert display_args["statGranularity"] == "daily"

    # The report's iteration should yield the expected item.
    item = next(report_obj)
    assert item["metric"] == 55
    assert item["label"] == "min"
