import datetime

from scheduleplus.scheduler import Scheduler


def test_cron_every_5_min():
    t0800 = datetime.datetime(2022, 1, 1, 8, 0, 0)
    sc = Scheduler().cron("*/5 * * * *", t0800)

    assert sc.next_run() == datetime.datetime(2022, 1, 1, 8, 5, 0)
