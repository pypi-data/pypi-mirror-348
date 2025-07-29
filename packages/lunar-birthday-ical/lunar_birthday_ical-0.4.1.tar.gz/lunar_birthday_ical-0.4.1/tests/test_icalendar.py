import datetime
import zoneinfo
from pathlib import Path

import yaml
from icalendar import Calendar, Event, vCalAddress, vText

from lunar_birthday_ical.config import (
    default_config,
    tests_config,
    tests_config_overwride_global,
)
from lunar_birthday_ical.icalendar import (
    add_attendees_to_event,
    add_event_to_calendar,
    add_reminders_to_event,
    create_calendar,
    get_local_datetime,
    local_datetime_to_utc_datetime,
)
from lunar_birthday_ical.utils import deep_merge_iterative


def test_get_local_datetime():
    local_date = "2023-10-01"
    local_time = "12:00:00"
    timezone = zoneinfo.ZoneInfo("UTC")
    result = get_local_datetime(local_date, local_time, timezone)
    expected = datetime.datetime(2023, 10, 1, 12, 0, tzinfo=timezone)
    assert result == expected


def test_local_datetime_to_utc_datetime():
    local_datetime = datetime.datetime(
        2023, 10, 1, 12, 0, tzinfo=zoneinfo.ZoneInfo("Asia/Shanghai")
    )
    result = local_datetime_to_utc_datetime(local_datetime)
    expected = datetime.datetime(2023, 10, 1, 4, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    assert result == expected


def test_add_reminders_to_event():
    event = Event()
    reminders = [1, 2]
    summary = "Test Event"
    add_reminders_to_event(event, reminders, summary)
    assert len(event.subcomponents) == 2


def test_add_attendees_to_event_one():
    event = Event()
    attendees = ["test@example.com"]
    add_attendees_to_event(event, attendees)
    assert (
        len(
            [event.get("ATTENDEE")]
            if isinstance(event.get("ATTENDEE"), vCalAddress)
            else event.get("ATTENDEE")
        )
        == 1
    )


def test_add_attendees_to_event_multi():
    event = Event()
    attendees = ["test@example.com", "test@example.net"]
    add_attendees_to_event(event, attendees)
    assert (
        len(
            [event.get("ATTENDEE")]
            if isinstance(event.get("ATTENDEE"), vCalAddress)
            else event.get("ATTENDEE")
        )
        == 2
    )


def test_add_event_to_calendar():
    calendar = Calendar()
    dtstart = datetime.datetime(2023, 10, 1, 12, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    dtend = dtstart + datetime.timedelta(hours=1)
    summary = "Test Event"
    description = "This is a test event."
    reminders = [1]
    attendees = ["test@example.com"]
    add_event_to_calendar(
        calendar, dtstart, dtend, summary, description, reminders, attendees
    )
    assert len(calendar.subcomponents) == 1


def test_create_calendar(tmp_path: Path):
    calendar_name = "test-calendar"
    config_file = tmp_path / f"{calendar_name}.yaml"

    config = deep_merge_iterative(default_config, tests_config)
    config_file.write_text(yaml.safe_dump(config))
    expected_output_file = config_file.with_suffix(".ics")

    create_calendar(config_file)
    assert expected_output_file.exists()

    with expected_output_file.open("rb") as f:
        calendar_data = f.read()
    calendar = Calendar.from_ical(calendar_data)
    assert len(calendar.subcomponents) > 0
    assert calendar.get("X-WR-CALNAME") == calendar_name


def test_create_calendar_with_override_timezone(tmp_path: Path):
    calendar_name = "test-calendar-override-global"
    config_file = tmp_path / f"{calendar_name}.yaml"

    config = deep_merge_iterative(default_config, tests_config_overwride_global)
    config_file.write_text(yaml.safe_dump(config))
    expected_output_file = config_file.with_suffix(".ics")

    create_calendar(config_file)
    assert expected_output_file.exists()

    with expected_output_file.open("rb") as f:
        calendar_data = f.read()
    calendar = Calendar.from_ical(calendar_data)

    assert len(calendar.subcomponents) > 0
    assert calendar.get("X-WR-CALNAME") == calendar_name
    assert calendar.get("X-WR-TIMEZONE") == vText(b"America/Los_Angeles")
