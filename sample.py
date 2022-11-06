import time

from scheduleplus.scheduler import Scheduler


def work(data):
    print(f"Working func {data}...")


def work2(data):
    print(f"Working callback {data}...")


schedule = Scheduler()

schedule.cron("* * * * *").do_function(work, "test")
schedule.cron("*/5 * * * *").do_callback({"message": "cool"})

schedule.list_jobs()


def do_meta(meta):
    print(f"-meta: {meta}")


while True:
    schedule.run_function_jobs()
    schedule.run_callback_jobs(work2)
    time.sleep(1)
