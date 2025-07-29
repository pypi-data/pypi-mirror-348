import calendar
import datetime

from lunar_birthday_ical.calendar import (
    get_fathers_day,
    get_mothers_day,
    get_thanksgiving_day,
    get_thanksgiving_day_by_region,
    get_weekdays_in_month,
)


def test_get_weekdays_in_month():
    # Test case: Get all Sundays in May 2023
    year = 2023
    month = 5
    weekday = calendar.SUNDAY
    expected_dates = [
        datetime.date(2023, 5, 7),
        datetime.date(2023, 5, 14),
        datetime.date(2023, 5, 21),
        datetime.date(2023, 5, 28),
    ]
    assert get_weekdays_in_month(weekday, year, month) == expected_dates


def test_get_mothers_day():
    # Test case: Mother's Day in 2023
    year = 2023
    expected_date = datetime.date(2023, 5, 14)
    assert get_mothers_day(year) == expected_date


def test_get_fathers_day():
    # Test case: Father's Day in 2023
    year = 2023
    expected_date = datetime.date(2023, 6, 18)
    assert get_fathers_day(year) == expected_date


def test_get_thanksgiving_day():
    # Test case: Thanksgiving Day in 2023 (US)
    year = 2023
    expected_date = datetime.date(2023, 11, 23)
    assert get_thanksgiving_day(year) == expected_date


def test_get_thanksgiving_day_by_region():
    # Test case: Thanksgiving Day in Germany (2023)
    year = 2023
    region = "DE"
    expected_date = datetime.date(2023, 10, 1)
    assert get_thanksgiving_day_by_region(year, region) == expected_date

    # Test case: Thanksgiving Day in Canada (2023)
    region = "CA"
    expected_date = datetime.date(2023, 10, 9)
    assert get_thanksgiving_day_by_region(year, region) == expected_date

    # Test case: Thanksgiving Day in Liberia (2023)
    region = "LR"
    expected_date = datetime.date(2023, 11, 2)
    assert get_thanksgiving_day_by_region(year, region) == expected_date

    # Test case: Thanksgiving Day in Norfolk Island (2023)
    region = "NF"
    expected_date = datetime.date(2023, 11, 29)
    assert get_thanksgiving_day_by_region(year, region) == expected_date

    # Test case: Thanksgiving Day in the US (2023)
    region = "US"
    expected_date = datetime.date(2023, 11, 23)
    assert get_thanksgiving_day_by_region(year, region) == expected_date

    # Test case: Thanksgiving Day in Brazil (2023)
    region = "BR"
    expected_date = datetime.date(2023, 11, 23)
    assert get_thanksgiving_day_by_region(year, region) == expected_date
