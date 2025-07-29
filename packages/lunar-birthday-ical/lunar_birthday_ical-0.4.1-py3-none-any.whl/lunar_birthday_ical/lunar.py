import datetime
import logging

from lunar_python import Lunar, LunarYear

logger = logging.getLogger(__name__)


def get_future_solar_datetime(
    past_solar_datetime: datetime.datetime, year: int
) -> datetime.datetime:
    """
    Convert past_solar_datetime to a lunar date, then replace the year of the lunar date
    """
    # 计算给定 公历日期 对应的 农历日期
    # .fromDate 所接受的类型为 datetime.datetime, 实际上处理后会把 time 部分丢弃
    lunar = Lunar.fromDate(past_solar_datetime)
    lunar_year = LunarYear.fromYear(year)

    # 获取闰月
    leap_month = lunar_year.getLeapMonth()

    # 确定目标年份的农历月
    if lunar.getMonth() > 0:
        lunar_month = lunar_year.getMonth(lunar.getMonth())
    elif abs(lunar.getMonth()) == leap_month:
        lunar_month = lunar_year.getMonth(lunar.getMonth())
    else:
        lunar_month = lunar_year.getMonth(abs(lunar.getMonth()))

    # 确定农历日
    lunar_day = min(lunar.getDay(), lunar_month.getDayCount())

    # 创建目标年份的农历日期
    future_lunar = Lunar.fromYmd(year, lunar_month.getMonth(), lunar_day)

    # 转换为公历日期, 恢复原本的时间和 timezone
    solar_time = past_solar_datetime.time()
    future_solar_datetime = datetime.datetime.strptime(
        future_lunar.getSolar().toYmd(), "%Y-%m-%d"
    ).replace(
        hour=solar_time.hour,
        minute=solar_time.minute,
        second=solar_time.second,
        tzinfo=past_solar_datetime.tzinfo,
    )

    return future_solar_datetime
