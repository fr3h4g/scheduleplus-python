import datetime
from datetime import datetime as dt

import pytest

from scheduleplus.cronparser import CronParser


def _run_test(crontab, now):
    cp = CronParser(crontab, now)
    now = now or datetime.datetime.now()
    return cp._get_next_run_time()


def test_get_next_run_time():
    now = dt(2022, 5, 5, 10, 10)
    assert _run_test("* * * * *", now) == dt(2022, 5, 5, 10, 11)
    assert _run_test("* * * * *", now) == dt(2022, 5, 5, 10, 11)
    assert _run_test("30 * * * *", now) == dt(2022, 5, 5, 10, 30)
    assert _run_test("1 1 * * *", now) == dt(2022, 5, 6, 1, 1)
    assert _run_test("1 1 3 * *", now) == dt(2022, 6, 3, 1, 1)
    assert _run_test("1 1 3 7 *", now) == dt(2022, 7, 3, 1, 1)
    assert _run_test("1 1 3 4 *", now) == dt(2023, 4, 3, 1, 1)
    assert _run_test("* * * 4 *", now) == dt(2023, 4, 1, 0, 0)

    now = dt(2022, 5, 2, 10, 10)
    assert _run_test("* * * * mon", now) == dt(2022, 5, 2, 10, 11)
    assert _run_test("* * * * 0", now) == dt(2022, 5, 2, 10, 11)
    assert _run_test("* * * * 1", now) == dt(2022, 5, 3, 0, 0)
    assert _run_test("* * * * 2", now) == dt(2022, 5, 4, 0, 0)
    assert _run_test("* * * * 3", now) == dt(2022, 5, 5, 0, 0)
    assert _run_test("* * * * 4", now) == dt(2022, 5, 6, 0, 0)
    assert _run_test("* * * * 5", now) == dt(2022, 5, 7, 0, 0)
    assert _run_test("* * * * 6", now) == dt(2022, 5, 8, 0, 0)

    now = dt(2022, 5, 2, 10, 10)
    assert _run_test("* * * * * 0", now) == dt(2022, 5, 2, 10, 11)
    assert _run_test("* * * * * 1", now) == dt(2022, 5, 26, 0, 0)

    now = dt(2022, 5, 7, 10, 10)
    assert _run_test("* * * * * 0", now) == dt(2022, 5, 9, 0, 0)

    assert _run_test("1 1 1 1 1 1", now) == dt(2030, 1, 1, 1, 1)

    now = dt(2022, 2, 2, 10, 10)
    assert _run_test("3 3 3 3 *", now) == dt(2022, 3, 3, 3, 3)

    now = dt(2023, 2, 2, 10, 10)
    assert _run_test("3 3 3 3 * *", now) == dt(2023, 3, 3, 3, 3)


def test_raises():
    now = dt(2022, 5, 7, 10, 10)
    with pytest.raises(ValueError):
        assert _run_test("1 1 1 1", now) == dt(2030, 1, 1, 1, 1)

    with pytest.raises(RecursionError):
        assert _run_test("1 1 1 1 1 0", now) == dt(2030, 1, 1, 1, 1)


def test_iter():
    now = dt(2022, 2, 2, 10, 10)
    crontab = "3 3 3 3 *"
    cp = CronParser(crontab, now)
    assert cp.iter() == dt(2022, 3, 3, 3, 3)
    assert cp.iter() == dt(2023, 3, 3, 3, 3)
    assert cp.iter() == dt(2024, 3, 3, 3, 3)
    assert cp.iter() == dt(2025, 3, 3, 3, 3)
    assert cp.iter() == dt(2026, 3, 3, 3, 3)
    assert cp.iter() == dt(2027, 3, 3, 3, 3)
    assert cp.iter() == dt(2028, 3, 3, 3, 3)
    assert cp.iter() == dt(2029, 3, 3, 3, 3)
    assert cp.iter() == dt(2030, 3, 3, 3, 3)
    assert cp.iter() == dt(2031, 3, 3, 3, 3)


def test_leap_year():
    # TODO: This is not working

    # now = dt(2022, 2, 1, 10, 10)
    # crontab = "0 0 29 2 *"
    # cp = CronParser(crontab, now)
    # assert cp.iter() == dt(2024, 2, 29, 0, 0)
    # assert cp.iter() == dt(2028, 2, 29, 0, 0)

    now = dt(2022, 2, 27, 10, 10)
    crontab = "0 0 * * *"
    cp = CronParser(crontab, now)
    assert cp.iter() == dt(2022, 2, 28, 0, 0)
    assert cp.iter() == dt(2022, 3, 1, 0, 0)

    now = dt(2024, 2, 27, 10, 10)
    crontab = "0 0 * * *"
    cp = CronParser(crontab, now)
    assert cp.iter() == dt(2024, 2, 28, 0, 0)
    assert cp.iter() == dt(2024, 2, 29, 0, 0)
    assert cp.iter() == dt(2024, 3, 1, 0, 0)


def test_last_weekday_of_month():
    now = dt(2022, 7, 1, 10, 10)
    crontab = "0 0 * * L"
    cp = CronParser(crontab, now)
    assert cp.iter() == dt(2022, 7, 29, 0, 0)


def test_first_weekday_of_month():
    now = dt(2022, 1, 1, 10, 10)
    crontab = "0 0 * * F"
    cp = CronParser(crontab, now)
    assert cp.iter() == dt(2022, 1, 3, 0, 0)


def test_last_day_of_month():
    now = dt(2022, 1, 1, 10, 10)
    crontab = "0 0 L * *"
    cp = CronParser(crontab, now)
    assert cp.iter() == dt(2022, 1, 31, 0, 0)
