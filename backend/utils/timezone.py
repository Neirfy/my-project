import zoneinfo
from datetime import datetime
from datetime import timezone as datetime_timezone

from core.config import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE):
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        """
        Текущее ремя с часовым поясом
        :return:
        """
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        """
        datetime Время в зависимости от часового пояса

        :param dt:
        :return:
        """
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        Временная строка для привязки ко времени часового пояса
        :param date_str:
        :param format_str:
        :return:
        """
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)

    @staticmethod
    def f_utc(dt: datetime) -> datetime:
        """
        Часовой пояс время в часовом поясе UTC (GMT)
        :param dt:
        :return:
        """
        return dt.astimezone(datetime_timezone.utc)


timezone = TimeZone()