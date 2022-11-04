import time

from scheduleplus.schedule import Scheduler


def func():
    print("Working...")


schedule = Scheduler()

schedule.cron("*/5 * * * *").do(func)

while True:
    schedule.run_jobs()
    time.sleep(1)
