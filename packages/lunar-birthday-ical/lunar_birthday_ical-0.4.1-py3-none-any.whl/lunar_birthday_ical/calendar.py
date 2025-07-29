import calendar
import datetime


# calendar on Python 3.11 has not implement calendar.Month yet
# https://github.com/python/cpython/blob/3.11/Lib/calendar.py#L40
class Month:
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


def get_weekdays_in_month(
    weekday: int = calendar.SUNDAY,
    year: int = datetime.date.today().year,
    month: int = datetime.date.today().month,
) -> datetime.date:
    cal = calendar.Calendar(calendar.SUNDAY)
    monthcal = cal.monthdatescalendar(year, month)
    month_weekdays = [
        day
        for week in monthcal
        for day in week
        if day.month == month and day.weekday() == weekday
    ]

    return month_weekdays


def get_mothers_day(year: int = datetime.date.today().year) -> datetime.date:
    """
    2nd Sunday in May
    """
    return get_weekdays_in_month(calendar.SUNDAY, year, Month.MAY)[1]


def get_fathers_day(year: int = datetime.date.today().year) -> datetime.date:
    """
    3rd Sunday in June
    """
    return get_weekdays_in_month(calendar.SUNDAY, year, Month.JUNE)[2]


def get_thanksgiving_day(year: int = datetime.date.today().year) -> datetime.date:
    """
    4th Thursday in November (United States and Brazil)
    """
    return get_weekdays_in_month(calendar.THURSDAY, year, Month.NOVEMBER)[3]


def get_thanksgiving_day_by_region(
    year: int = datetime.date.today().year, region="US"
) -> datetime.date:
    """
    Return Thanksgiving day by Region,

    1st Sunday in October (Germany)
    2nd Monday in October (Canada)
    1st Thursday in November (Liberia)
    Last Wednesday in November (Norfolk Island)
    4th Thursday in November (United States and Brazil)
    """
    # weekday, month, weekday_index (0-index) region_rules
    region_rules = {
        "DE": (calendar.SUNDAY, Month.OCTOBER, 0),
        "CA": (calendar.MONDAY, Month.OCTOBER, 1),
        "LR": (calendar.THURSDAY, Month.NOVEMBER, 0),
        "NF": (calendar.WEDNESDAY, Month.NOVEMBER, -1),
        "US": (calendar.THURSDAY, Month.NOVEMBER, 3),
        "BR": (calendar.THURSDAY, Month.NOVEMBER, 3),
    }

    weekday, month, weekday_index = region_rules[region]
    return get_weekdays_in_month(weekday, year, month)[weekday_index]


holiday_callout = {
    "mothers_day": {
        "summary": "母亲节",
        "description": "母亲节 (英语: Mother's Day), 是一个为感谢母亲而庆祝的节日, 而在世界各地的母亲节的日期有所不同. 母亲们在这一天里通常会收到孩子们送的礼物; 而在许多人心目中, 象征花康乃馨被视为作最适合献给母亲的鲜花之一. 母亲节是一个向母亲表达感谢和爱意的特殊时刻. 无论是你的妈妈, 岳母, 外婆还是任何其他特别的母亲, 许多人都会在母亲节送一份有心思的礼物让对方感到幸福与专属感.",
        "callout": get_mothers_day,
    },
    "fathers_day": {
        "summary": "父亲节",
        "description": "父亲节 (英语: Father's Day), 是一个为感谢父亲而庆祝的节日, 世界各地因不同的历史, 文化原因选在不同日期. 孩子们在这一天里通常会送礼物给父亲. 其中以 6 月的第三个星期日为父亲节的国家与地区最多, 包括欧亚及美洲的超过 80 个国家或地区. 中国大陆没有设立正式的父亲节, 但港澳民众习惯上和欧美一样使用 6 月第三个星期日, 而中国大陆民间也自改革开放后开始以 6 月第三个星期日作为父亲节. 台湾自从战后时期起, 以及中国大陆在民国时期, 采用 8 月 8 日. 有许多国家都把石斛兰作为'父亲节之花'.",
        "callout": get_fathers_day,
    },
    "thanksgiving_day": {
        "summary": "感恩节",
        "description": "感恩节 (英语: Thanksgiving Day), 是位于北美的美国与加拿大的全国节日, 源自基督教. 目的是感谢上帝过去一年的赠与和丰收. 加拿大和美国的感恩节时间并不相同.",
        "callout": get_thanksgiving_day,
    },
}
