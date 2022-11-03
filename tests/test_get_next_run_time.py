import datetime
from datetime import datetime as dt
from scheduleplus.cronparser import CronParser


def _run_test(crontab, now):
    cp = CronParser(crontab, now)
    now = now or datetime.datetime.now()
    return cp.next()


def test_get_next_run_time():
    now = dt(2022, 5, 5, 10, 10)
    assert _run_test("*  * * * *", now) == dt(2022, 5, 5, 10, 11)
    assert _run_test("*  * * * *", now) == dt(2022, 5, 5, 10, 11)
    assert _run_test("30 * * * *", now) == dt(2022, 5, 5, 10, 30)
    assert _run_test("1  1 * * *", now) == dt(2022, 5, 6, 1, 1)
    assert _run_test("1  1 3 * *", now) == dt(2022, 6, 3, 1, 1)
    assert _run_test("1  1 3 7 *", now) == dt(2022, 7, 3, 1, 1)
    assert _run_test("1  1 3 4 *", now) == dt(2023, 4, 3, 1, 1)
    assert _run_test("*  * * 4 *", now) == dt(2023, 4, 1, 0, 0)
