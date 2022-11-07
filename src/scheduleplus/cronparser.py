import datetime
import calendar
from datetime import timedelta

from workalendar.europe import Sweden

RANGES = [
    (0, 59),
    (0, 23),
    (1, 31),
    (1, 12),
    (0, 6),
    (0, 1),
]

ATTRIBUTES = [
    "minute",
    "hour",
    "day",
    "month",
    "weekday",
]

ALIASES = {
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@hourly": "0 * * * *",
}

ISODAYS = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


class CronParser:
    def __init__(self, cron_str: str, now=None, wk_country=None):
        if not wk_country:
            wk_country = Sweden()
        self._wk_country = wk_country
        # self._wk_country = self._wk_country
        self._cron_str = cron_str
        self._next_run_time = datetime.datetime.now()
        if now:
            self._next_run_time = now
        self._next_run_time = self._next_run_time.replace(second=0, microsecond=0)
        self._next_run_time += timedelta(minutes=1)

    def _trim_extra_whitespace(self):
        return " ".join(self._cron_str.split())

    def _parse_cron_str(self):
        parsed_cron_data = []
        self._cron_str = self._trim_extra_whitespace()
        self._cron_str = self._replace_alias()
        for part_index, part_str in enumerate(self._cron_str.split(" ")):
            parsed_cron_data.append(self._parse_part(part_str, part_index))
        return parsed_cron_data

    def _replace_alias(self):
        cron_str = self._cron_str.lower()
        for index in ALIASES:
            if index in cron_str:
                cron_str = ALIASES[index]
        return cron_str

    def _replace_month_day(self, part_str: str, part_index: int):
        part_str = part_str.lower()
        if part_index == 4:
            for index, day in enumerate(ISODAYS):
                part_str = part_str.replace(day, str(index))
        elif part_index == 3:
            for index, month in enumerate(MONTHS):
                part_str = part_str.replace(month, str(index + 1))
        return part_str

    def _parse_part(self, part_str: str, part_index: int):
        part_str = self._replace_month_day(part_str, part_index)
        return_list = []
        for part in part_str.split(","):
            start, end, step = RANGES[part_index][0], RANGES[part_index][1] + 1, 1
            if part == "*":
                for num in range(start, end, step):
                    if num not in return_list:
                        return_list.append(num)
            elif "/" in part:
                tmp = part.split("/")
                if tmp[0] != "*":
                    if "-" in tmp[0]:
                        tmp2 = tmp[0].split("-")
                        start, end = int(tmp2[0]), int(tmp2[1]) + 1
                    else:
                        start, end = int(tmp[0]), RANGES[part_index][1] + 1
                step = int(tmp[1])
                for num in range(start, end, step):
                    if num not in return_list:
                        return_list.append(num)
            elif "-" in part:
                tmp2 = part.split("-")
                start, end = int(tmp2[0]), int(tmp2[1]) + 1
                for num in range(start, end, step):
                    if num not in return_list:
                        return_list.append(num)
            elif part_str.upper() == "F":
                return_list.append("F")
            elif part_str.upper() == "L":
                return_list.append("L")
            else:
                if int(part) not in return_list and int(part) in range(
                    RANGES[part_index][0], RANGES[part_index][1] + 1
                ):
                    return_list.append(int(part))
        return_list.sort()
        return return_list

    def _proc_minute(self, index, parsed_data):
        for num in parsed_data[index]:
            if num >= self._next_run_time.minute:
                self._next_run_time = self._next_run_time.replace(minute=num)
                break
        else:
            self._next_run_time = self._next_run_time + timedelta(hours=1)
            self._next_run_time = self._next_run_time.replace(minute=0)
            self._next_run_time = self._proc_minute(index, parsed_data)
        return self._next_run_time

    def _proc_hour(self, index, parsed_data):
        for num in parsed_data[index]:
            if num >= self._next_run_time.hour:
                self._next_run_time = self._next_run_time.replace(hour=num)
                break
        else:
            self._next_run_time = self._next_run_time + timedelta(days=1)
            self._next_run_time = self._next_run_time.replace(minute=0)
            self._next_run_time = self._next_run_time.replace(hour=0)
            self._next_run_time = self._proc_minute(0, parsed_data)
            self._next_run_time = self._proc_hour(index, parsed_data)
        return self._next_run_time

    def _proc_day(self, index, parsed_data):
        if parsed_data[index] == ["L"]:
            days_of_month = calendar.monthrange(
                self._next_run_time.month, self._next_run_time.month
            )[1]
            if days_of_month == self._next_run_time.day:
                self._next_run_time = self._next_run_time + timedelta(days=1)
            self._next_run_time = self._next_run_time.replace(day=days_of_month)
            # self._next_run_time = self._next_run_time - timedelta(days=1)
        else:
            for num in parsed_data[index]:
                if num >= self._next_run_time.day:
                    self._next_run_time = self._next_run_time.replace(day=num)
                    break
            else:
                self._next_run_time = self._next_run_time.replace(day=1)
                self._next_run_time = self._next_run_time + timedelta(days=32)
                self._next_run_time = self._next_run_time.replace(day=1)
                self._next_run_time = self._next_run_time.replace(minute=0)
                self._next_run_time = self._next_run_time.replace(hour=0)
                self._next_run_time = self._proc_minute(0, parsed_data)
                self._next_run_time = self._proc_hour(1, parsed_data)
                self._next_run_time = self._proc_day(index, parsed_data)
        return self._next_run_time

    def _incr_year(self):
        mod = self._next_run_time.year % 4
        if mod == 0 and (self._next_run_time.month, self._next_run_time.day) < (2, 29):
            return timedelta(days=365 + 1)
        if mod == 3 and (self._next_run_time.month, self._next_run_time.day) > (2, 29):
            return timedelta(days=365 + 1)
        return timedelta(days=365)

    def _proc_month(self, index, parsed_data):
        for num in parsed_data[index]:
            if num >= self._next_run_time.month:
                self._next_run_time = self._next_run_time.replace(month=num)
                break
        else:
            self._next_run_time = self._next_run_time + self._incr_year()
            self._next_run_time = self._next_run_time.replace(month=1)
            self._next_run_time = self._next_run_time.replace(day=1)
            self._next_run_time = self._next_run_time.replace(minute=0)
            self._next_run_time = self._next_run_time.replace(hour=0)
            self._next_run_time = self._proc_minute(0, parsed_data)
            self._next_run_time = self._proc_hour(1, parsed_data)
            self._next_run_time = self._proc_day(2, parsed_data)
            self._next_run_time = self._proc_month(index, parsed_data)
        return self._next_run_time

    def _proc_weekday(self, index, parsed_data):
        if self._next_run_time.weekday() in parsed_data[index]:
            return self._next_run_time
        else:
            if parsed_data[index] == ["F"]:
                self._next_run_time = self._next_run_time + timedelta(days=32)
                self._next_run_time = self._next_run_time.replace(day=1)
                while not self._wk_country.is_working_day(self._next_run_time.date()):
                    self._next_run_time = self._next_run_time + timedelta(days=1)
            elif parsed_data[index] == ["L"]:
                days_of_month = calendar.monthrange(
                    self._next_run_time.month, self._next_run_time.month
                )[1]
                self._next_run_time = self._next_run_time.replace(day=days_of_month)
                while not self._wk_country.is_working_day(self._next_run_time.date()):
                    self._next_run_time = self._next_run_time - timedelta(days=1)
                if self._last_run_time >= self._next_run_time:
                    self._next_run_time = self._next_run_time + timedelta(days=32)
                    self._next_run_time = self._next_run_time.replace(day=days_of_month)
                    while not self._wk_country.is_working_day(
                        self._next_run_time.date()
                    ):
                        self._next_run_time = self._next_run_time - timedelta(days=1)
            else:
                while self._next_run_time.weekday() not in parsed_data[index]:
                    self._next_run_time = self._next_run_time + timedelta(days=1)
                    self._next_run_time = self._next_run_time.replace(minute=0)
                    self._next_run_time = self._next_run_time.replace(hour=0)
                    self._next_run_time = self._get_next_run_time()
        return self._next_run_time

    def _proc_holiday(self, index, parsed_data):
        if [0, 1] == parsed_data[index]:
            return self._next_run_time
        if 0 in parsed_data[index]:
            if self._wk_country.is_working_day(self._next_run_time.date()):
                return self._next_run_time
            else:
                while not self._wk_country.is_working_day(self._next_run_time.date()):
                    self._next_run_time = self._next_run_time + timedelta(days=1)
                    self._next_run_time = self._next_run_time.replace(minute=0)
                    self._next_run_time = self._next_run_time.replace(hour=0)
                    self._next_run_time = self._get_next_run_time()
        if 1 in parsed_data[index]:
            if self._wk_country.is_holiday(self._next_run_time.date()):
                return self._next_run_time
            else:
                while not self._wk_country.is_holiday(self._next_run_time.date()):
                    self._next_run_time = self._next_run_time + timedelta(days=1)
                    self._next_run_time = self._next_run_time.replace(minute=0)
                    self._next_run_time = self._next_run_time.replace(hour=0)
                    self._next_run_time = self._get_next_run_time()
        return self._next_run_time

    def _get_next_run_time(self):
        self._last_run_time = self._next_run_time
        parsed_data = self._parse_cron_str()
        if len(parsed_data) < 5:
            raise ValueError("Error in cron string, not 5 or 6 values")
        for index in range(0, len(parsed_data)):
            if index == 0:
                self._next_run_time = self._proc_minute(index, parsed_data)
            if index == 1:
                self._next_run_time = self._proc_hour(index, parsed_data)
            if index == 2:
                self._next_run_time = self._proc_day(index, parsed_data)
            if index == 3:
                self._next_run_time = self._proc_month(index, parsed_data)
            if index == 4:
                self._next_run_time = self._proc_weekday(index, parsed_data)
            if index == 5:
                self._next_run_time = self._proc_holiday(index, parsed_data)
        return self._next_run_time

    def iter(self):
        self._next_run_time += timedelta(minutes=1)
        return self._get_next_run_time()

    def next_run_time(self):
        return self._get_next_run_time()
