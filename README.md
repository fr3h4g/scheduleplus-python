# scheduleplus

A scheduler built on cron syntax with weekend/holiday features

| Atributes | Allowed values | Allowed special characters |
| --------- | -------------- | -------------------------- |
| Minutes   | 0-59           | \* , - /                   |
| Hours     | 0-23           | \* , - /                   |
| Days      | 1-31           | \* , - /                   |
| Months    | 1-12, JAN-DEC  | \* , - /                   |
| Weekdays  | 0-6, MON-SUN   | \* , - /                   |
| Holiday   | 0, 1           | \*                         |

## Installation

```
pip install scheduleplus
```

## Usage

### Running a function on schedule

Running a function every 5 minutes.

```python
from scheduleplus.schedule import Scheduler

def work(data):
    print(f"Working {data}...")

schedule = Scheduler()

schedule.cron("*/5 * * * *").do_function(work, "test")

while True:
    schedule.run_function_jobs()
    time.sleep(1)
```

### Running a callback

Running callback with a dictonary every 5 minutes.

```python
from scheduleplus.schedule import Scheduler

def work(data):
    print(f"Working {data}...")

schedule = Scheduler()

schedule.cron("*/5 * * * *").do_callback({"message": "cool"})

while True:
    schedule.run_callback_jobs(work)
    time.sleep(1)
```

### List jobs

```python
schedule = Scheduler()

schedule.cron("*/5 * * * *").do_function(work, "test")
schedule.cron("*/5 * * * *").do_callback({"message": "cool"})

schedule.list_jobs()
```

Result

```shell
Job id   Cron          Next run time         Time left             Function        Callback message
-------- ------------- --------------------- --------------------- --------------- ---------------------
1        */5 * * * *   2022-11-04 13:50:00   0:00:29               work('test')
2        1 1 1 1 1     2030-01-01 01:01:00   2614 days, 11:11:29                   {'message': 'cool'}
```
