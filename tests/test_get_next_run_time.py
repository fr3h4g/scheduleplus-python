from datetime import datetime as dt
from scheduleplus.util import _get_next_run_time


def test_get_next_run_time():
    now = dt(2022, 5, 5, 10, 10)
    assert _get_next_run_time("*  * * * *", now) == dt(2022, 5, 5, 10, 11)
    assert _get_next_run_time("30 * * * *", now) == dt(2022, 5, 5, 10, 30)
    assert _get_next_run_time("1 1 * * *", now) == dt(2022, 5, 6, 1, 1)
    assert _get_next_run_time("1 1 3 * *", now) == dt(2022, 6, 3, 1, 1)
    assert _get_next_run_time("1 1 3 7 *", now) == dt(2022, 7, 3, 1, 1)
    assert _get_next_run_time("1 1 3 4 *", now) == dt(2023, 4, 3, 1, 1)
    assert _get_next_run_time("* * * 4 *", now) == dt(2023, 4, 1, 0, 0)
