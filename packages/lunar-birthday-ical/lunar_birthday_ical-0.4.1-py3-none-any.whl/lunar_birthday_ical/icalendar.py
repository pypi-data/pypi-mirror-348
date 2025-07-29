import datetime
import json
import logging
import uuid
import zoneinfo
from pathlib import Path

import icalendar
import yaml
from lunar_python import Solar

from lunar_birthday_ical.calendar import holiday_callout
from lunar_birthday_ical.config import default_config
from lunar_birthday_ical.lunar import get_future_solar_datetime
from lunar_birthday_ical.pastebin import pastebin_helper
from lunar_birthday_ical.utils import deep_merge_iterative

logger = logging.getLogger(__name__)


def get_local_datetime(
    local_date: datetime.date | str,
    local_time: datetime.time | str,
    timezone: zoneinfo.ZoneInfo,
) -> datetime.datetime:
    if not isinstance(local_date, datetime.date):
        local_date = datetime.datetime.strptime(local_date, "%Y-%m-%d").date()
    if not isinstance(local_time, datetime.time):
        local_time = datetime.datetime.strptime(local_time, "%H:%M:%S").time()

    local_datetime = datetime.datetime.combine(local_date, local_time, timezone)

    return local_datetime


def local_datetime_to_utc_datetime(
    local_datetime: datetime.datetime,
) -> datetime.datetime:
    # 将 local_datetime "强制"转换为 UTC 时间, 注意 local_datetime 需要携带 tzinfo 信息
    utc = zoneinfo.ZoneInfo("UTC")
    # 这里宁可让它抛出错误信息, 也不要设置 默认值
    utc_datetime = local_datetime.replace(tzinfo=utc) - local_datetime.utcoffset()

    return utc_datetime


def add_reminders_to_event(
    event: icalendar.Event, reminders: list[int | datetime.datetime], summary: str
) -> None:
    # 添加提醒
    for reminder_days in reminders:
        if isinstance(reminder_days, datetime.datetime):
            trigger_time = reminder_days
        elif isinstance(reminder_days, int):
            trigger_time = datetime.timedelta(days=-reminder_days)
        else:
            continue
        alarm = icalendar.Alarm()
        alarm.add("uid", uuid.uuid4())
        alarm.add("action", "DISPLAY")
        alarm.add("description", f"Reminder: {summary}")
        alarm.add("trigger", trigger_time)
        event.add_component(alarm)


def add_attendees_to_event(event: icalendar.Event, attendees: list[str]) -> None:
    # 添加与会者
    for attendee_email in attendees:
        attendee = icalendar.vCalAddress(f"mailto:{attendee_email}")
        attendee.params["cn"] = icalendar.vText(attendee_email.split("@")[0])
        attendee.params["role"] = icalendar.vText("REQ-PARTICIPANT")
        event.add("attendee", attendee)


def add_event_to_calendar(
    calendar: icalendar.Calendar,
    dtstart: datetime.datetime,
    dtend: datetime.datetime,
    summary: str,
    description: str,
    reminders: list[int | datetime.datetime],
    attendees: list[str],
) -> None:
    event = icalendar.Event()
    event.add("uid", uuid.uuid4())
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    event.add("dtstamp", icalendar.vDatetime(now_utc))
    event.add("dtstart", icalendar.vDatetime(dtstart))
    event.add("dtend", icalendar.vDatetime(dtend))
    event.add("summary", summary)
    event.add("description", description)

    add_reminders_to_event(event, reminders, summary)
    add_attendees_to_event(event, attendees)

    calendar.add_component(event)


def add_integer_days_event(calendar: icalendar.Calendar, item_config: dict) -> None:
    timezone = zoneinfo.ZoneInfo(item_config.get("timezone"))
    # YAML 似乎会自动将 YYYY-mm-dd 格式字符串转换成 datetime.date 类型
    start_date = item_config.get("start_date")
    event_time = item_config.get("event_time")
    # 开始时间, 类型为 datetime.datetime
    start_datetime = get_local_datetime(start_date, event_time, timezone)
    # 事件持续时长
    event_hours = datetime.timedelta(hours=item_config.get("event_hours"))

    name = item_config.get("name")
    year_start = item_config.get("year_start") or datetime.date.today().year
    year_end = item_config.get("year_end")

    days_max = item_config.get("days_max")
    days_interval = item_config.get("days_interval")

    integer_days_summary = "{name} 降临地球🌏已经 {days} 天啦!"
    integer_days_description = (
        "{name} 降临地球🌏已经 {days} 天啦! (age: {age}, birthday: {birthday})"
    )
    summary = item_config.get("summary") or integer_days_summary
    description = item_config.get("description") or integer_days_description

    for days in range(days_interval, days_max + 1, days_interval):
        # 整数日事件 将 start_datetime 加上间隔 days 即可
        event_datetime = start_datetime + datetime.timedelta(days=days)
        # 跳过在 [year_start, year_end] 之外的事件
        if event_datetime.year < year_start or event_datetime.year > year_end:
            continue

        # iCal 中的时间都以 UTC 保存
        dtstart = local_datetime_to_utc_datetime(event_datetime)
        dtend = dtstart + event_hours
        year_average = 365.25
        age = round(days / year_average, 2)

        reminders_datetime = [
            dtstart - datetime.timedelta(days=days)
            for days in item_config.get("reminders")
        ]
        add_event_to_calendar(
            calendar=calendar,
            dtstart=dtstart,
            dtend=dtend,
            summary=summary.format(name=name, days=days),
            description=description.format(
                name=name, days=days, age=age, birthday=start_date
            ),
            reminders=reminders_datetime,
            attendees=item_config.get("attendees"),
        )


def add_birthday_event(calendar: icalendar.Calendar, item_config: dict) -> None:
    timezone = zoneinfo.ZoneInfo(item_config.get("timezone"))
    # YAML 似乎会自动将 YYYY-mm-dd 格式字符串转换成 datetime.date 类型
    start_date = item_config.get("start_date")
    event_time = item_config.get("event_time")
    # 开始时间, 类型为 datetime.datetime
    start_datetime = get_local_datetime(start_date, event_time, timezone)
    start_datetime_in_lunar = Solar.fromDate(start_datetime).getLunar()
    event_hours = datetime.timedelta(hours=item_config.get("event_hours"))

    name = item_config.get("name")
    year_start = item_config.get("year_start") or datetime.date.today().year
    year_end = item_config.get("year_end")

    for event_key in item_config.get("event_keys") or []:
        if event_key not in ["solar_birthday", "lunar_birthday"]:
            continue

        if event_key == "solar_birthday":
            birthday = start_date
            birthday_summary = "{name} {year} 年生日🎂快乐!"
            birthday_description = (
                "{name} {year} 年生日🎂快乐! (age: {age}, birthday: {birthday})"
            )
        elif event_key == "lunar_birthday":
            birthday = start_datetime_in_lunar
            birthday_summary = "{name} {year} 年农历生日🎂快乐!"
            birthday_description = (
                "{name} {year} 年农历生日🎂快乐! (age: {age}, birthday: {birthday})"
            )

        summary = item_config.get("summary") or birthday_summary
        description = item_config.get("description") or birthday_description

        for year in range(year_start, year_end + 1):
            age = year - start_datetime.year
            if event_key == "solar_birthday":
                event_datetime = start_datetime.replace(year=year)
            elif event_key == "lunar_birthday":
                event_datetime = get_future_solar_datetime(start_datetime, year)

            dtstart = local_datetime_to_utc_datetime(event_datetime)
            dtend = dtstart + event_hours
            reminders_datetime = [
                dtstart - datetime.timedelta(days=days)
                for days in item_config.get("reminders")
            ]
            add_event_to_calendar(
                calendar=calendar,
                dtstart=dtstart,
                dtend=dtend,
                summary=summary.format(
                    name=name,
                    year=year,
                ),
                description=description.format(
                    name=name,
                    year=year,
                    age=age,
                    birthday=birthday,
                ),
                reminders=reminders_datetime,
                attendees=item_config.get("attendees"),
            )


def add_holiday_event(calendar: icalendar.Calendar, global_config: dict) -> None:
    timezone = zoneinfo.ZoneInfo(global_config.get("timezone"))
    event_time = global_config.get("event_time")
    event_hours = datetime.timedelta(hours=global_config.get("event_hours"))

    year_start = global_config.get("year_start")
    year_end = global_config.get("year_end")

    for holiday_key, holiday_value in holiday_callout.items():
        if holiday_key not in global_config.get("holiday_keys") or []:
            continue

        for year in range(year_start, year_end + 1):
            event_date = holiday_value.get("callout")(year)
            event_datetime = get_local_datetime(event_date, event_time, timezone)
            dtstart = local_datetime_to_utc_datetime(event_datetime)
            dtend = dtstart + event_hours
            reminders_datetime = [
                dtstart - datetime.timedelta(days=days)
                for days in global_config.get("reminders")
            ]
            add_event_to_calendar(
                calendar=calendar,
                dtstart=dtstart,
                dtend=dtend,
                summary=holiday_value.get("summary"),
                description=holiday_value.get("description"),
                reminders=reminders_datetime,
                attendees=global_config.get("attendees"),
            )


def create_calendar(config_file: Path) -> None:
    with open(config_file, "r") as f:
        yaml_config = yaml.safe_load(f)
        merged_config = deep_merge_iterative(default_config, yaml_config)
        logger.debug(
            "merged_config=%s",
            json.dumps(merged_config, ensure_ascii=False, default=str),
        )

    global_config = merged_config.get("global")

    calendar = icalendar.Calendar()
    calendar_name = config_file.stem
    timezone = zoneinfo.ZoneInfo(global_config.get("timezone"))
    calendar.add("PRODID", "-//ak1ra-lab//lunar-birthday-ical//EN")
    calendar.add("VERSION", "2.0")
    calendar.add("CALSCALE", "GREGORIAN")
    calendar.add("X-WR-CALNAME", calendar_name)
    calendar.add("X-WR-TIMEZONE", timezone)

    for item in merged_config.get("events"):
        item_config = deep_merge_iterative(global_config, item)
        event_keys = item_config.get("event_keys")

        if "integer_days" in event_keys:
            add_integer_days_event(calendar, item_config)

        add_birthday_event(calendar, item_config)

    add_holiday_event(calendar, global_config)

    calendar_data = calendar.to_ical()
    output = config_file.with_suffix(".ics")
    with output.open("wb") as f:
        f.write(calendar_data)
    logger.info("iCal saved to %s", output)

    if merged_config.get("pastebin").get("enabled", False):
        pastebin_helper(merged_config, output)
