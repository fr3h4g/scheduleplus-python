import time

from scheduleplus.schedule import Scheduler


def func(hej="", test=""):
    print(f"Working func {hej} {test}...")


def cool(hej="", test=""):
    print(f"Working cool {hej} {test}...")


schedule = Scheduler()

schedule.cron("1 1 1 1 1").do_function(cool, "cool", "-")
schedule.cron("* * * * *").do_function(func, 10, 20)
schedule.cron("1 1 1 1 1").do_function(cool, "cool", "-")
schedule.cron("* * * * * ").do_callback({"message": "cool"})

schedule.list_jobs()


def do_meta(meta):
    print(f"-meta: {meta}")


while True:
    schedule.run_function_jobs()
    schedule.run_callback_jobs(do_meta)
    time.sleep(1)
