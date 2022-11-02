import datetime
from scheduleplus.schedule import Scheduler


def test_cron_every_5_min():
    sc = Scheduler().cron("*/5 * * * *")

    t0800 = datetime.datetime(2022, 1, 1, 8, 0, 0)

    assert sc.next_run(t0800) == datetime.datetime(2022, 1, 1, 8, 5, 0)
