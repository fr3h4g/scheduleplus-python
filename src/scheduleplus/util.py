import datetime
from datetime import timedelta


RANGES = [
    (0, 59),
    (0, 23),
    (1, 31),
    (1, 12),
    (0, 6),
]

ATTRIBUTES = [
    "minute",
    "hour",
    "day",
    "month",
    "isoweekday",
]

ALIASES = {
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@hourly": "0 * * * *",
}

ISODAYS = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6}
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


def _tris_extra_whitespace(str):
    return " ".join(str.split())


def _parse_cron_str(cron_str: str):
    parsed_cron_data = []
    cron_str = _tris_extra_whitespace(cron_str)
    cron_str = _replace_alias(cron_str)
    for part_index, part_str in enumerate(cron_str.split(" ")):
        parsed_cron_data.append(_parse_part(part_str, part_index))
    return parsed_cron_data


def _replace_alias(cron_str: str):
    cron_str = cron_str.lower()
    for index in ALIASES:
        if index in cron_str:
            cron_str = ALIASES[index]
    return cron_str


def _replace_month_day(part_str: str, part_index: int):
    part_str = part_str.lower()
    if part_index == 4:
        for index, day in enumerate(ISODAYS):
            part_str = part_str.replace(day, str(index))
    elif part_index == 3:
        for index, month in enumerate(MONTHS):
            part_str = part_str.replace(month, str(index + 1))
    return part_str


def _parse_part(part_str: str, part_index: int):
    part_str = _replace_month_day(part_str, part_index)
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
        else:
            if int(part) not in return_list and int(part) in range(
                RANGES[part_index][0], RANGES[part_index][1] + 1
            ):
                return_list.append(int(part))
    return_list.sort()
    return return_list


def _proc_minute(index, parsed_data, next_run_time: datetime.datetime):
    for num in parsed_data[index]:
        if num >= next_run_time.minute:
            next_run_time = next_run_time.replace(minute=num)
            break
    else:
        next_run_time = next_run_time + timedelta(hours=1)
        next_run_time = next_run_time.replace(minute=0)
        next_run_time = _proc_minute(index, parsed_data, next_run_time)
    return next_run_time


def _proc_hour(index, parsed_data, next_run_time: datetime.datetime):
    for num in parsed_data[index]:
        if num >= next_run_time.hour:
            next_run_time = next_run_time.replace(hour=num)
            break
    else:
        next_run_time = next_run_time + timedelta(days=1)
        next_run_time = next_run_time.replace(minute=0)
        next_run_time = next_run_time.replace(hour=0)
        next_run_time = _proc_minute(0, parsed_data, next_run_time)
        next_run_time = _proc_hour(index, parsed_data, next_run_time)
    return next_run_time


def _proc_day(index, parsed_data, next_run_time: datetime.datetime):
    for num in parsed_data[index]:
        if num >= next_run_time.day:
            next_run_time = next_run_time.replace(day=num)
            break
    else:
        next_run_time = next_run_time.replace(day=1)
        next_run_time = next_run_time + timedelta(days=32)
        next_run_time = next_run_time.replace(day=1)
        next_run_time = next_run_time.replace(minute=0)
        next_run_time = next_run_time.replace(hour=0)
        next_run_time = _proc_minute(0, parsed_data, next_run_time)
        next_run_time = _proc_hour(1, parsed_data, next_run_time)
        next_run_time = _proc_day(index, parsed_data, next_run_time)
    return next_run_time


def _incr_year(next_run_time):
    mod = next_run_time.year % 4
    if mod == 0 and (next_run_time.month, next_run_time.day) < (2, 29):
        return timedelta(days=365 + 1)
    if mod == 3 and (next_run_time.month, next_run_time.day) > (2, 29):
        return timedelta(days=365 + 1)
    return timedelta(days=365)


def _proc_month(index, parsed_data, next_run_time: datetime.datetime):
    for num in parsed_data[index]:
        if num >= next_run_time.month:
            next_run_time = next_run_time.replace(month=num)
            break
    else:
        next_run_time = next_run_time.replace(month=1)
        next_run_time = next_run_time + _incr_year(next_run_time)
        next_run_time = next_run_time.replace(month=1)
        next_run_time = next_run_time.replace(day=1)
        next_run_time = next_run_time.replace(minute=0)
        next_run_time = next_run_time.replace(hour=0)
        next_run_time = _proc_minute(0, parsed_data, next_run_time)
        next_run_time = _proc_hour(1, parsed_data, next_run_time)
        next_run_time = _proc_day(2, parsed_data, next_run_time)
        next_run_time = _proc_month(index, parsed_data, next_run_time)
    return next_run_time


def _proc_weekday(index, parsed_data, next_run_time: datetime.datetime, cron_str):
    if next_run_time.weekday() in parsed_data[index]:
        return next_run_time
    for num in parsed_data[index]:
        num = num - 1
        if num < 0:
            num = 6
        if num == next_run_time.weekday():
            break
        else:
            while num != next_run_time.weekday():
                next_run_time = next_run_time + timedelta(days=1)
                next_run_time = next_run_time.replace(minute=0)
                next_run_time = next_run_time.replace(hour=0)
                next_run_time = _get_next_run_time(cron_str, now=next_run_time)
    return next_run_time


def _get_next_run_time(cron_str: str, now=None):
    parsed_data = _parse_cron_str(cron_str)
    if not now:
        now = datetime.datetime.now()
    next_run_time = now + timedelta(minutes=1)
    next_run_time = next_run_time.replace(second=0, microsecond=0)
    for index in range(0, 5):
        if index == 0:
            next_run_time = _proc_minute(index, parsed_data, next_run_time)
        if index == 1:
            next_run_time = _proc_hour(index, parsed_data, next_run_time)
        if index == 2:
            next_run_time = _proc_day(index, parsed_data, next_run_time)
        if index == 3:
            next_run_time = _proc_month(index, parsed_data, next_run_time)
        if index == 4:
            next_run_time = _proc_weekday(index, parsed_data, next_run_time, cron_str)
    return next_run_time


def _iter(cron_str: str):
    now = datetime.datetime.now()
    for _ in range(1, 11):
        now = _get_next_run_time(cron_str, now)
        yield now


if __name__ == "__main__":
    cron = _iter("* * * * *")
    for row in cron:
        print(row)
