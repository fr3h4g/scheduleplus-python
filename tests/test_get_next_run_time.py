import datetime
from datetime import datetime as dt
from scheduleplus.cronparser import CronParser


def _run_test(crontab, now):
    cp = CronParser(crontab, now)
    now = now or datetime.datetime.now()
    return cp.next()


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
    # assert _run_test("* * * * 1", now) == dt(2022, 5, 2, 10, 11)
    # assert _run_test("* * * * 2", now) == dt(2022, 5, 3, 0, 0)
    # assert _run_test("* * * * 3", now) == dt(2022, 5, 4, 0, 0)
    # assert _run_test("* * * * 4", now) == dt(2022, 5, 5, 0, 0)
    # assert _run_test("* * * * 5", now) == dt(2022, 5, 6, 0, 0)
    # assert _run_test("* * * * 6", now) == dt(2022, 5, 7, 0, 0)
    # assert _run_test("* * * * 7", now) == dt(2022, 5, 8, 0, 0)
