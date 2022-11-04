import datetime
import json
from datetime import timedelta

from scheduleplus.cronparser import CronParser
from scheduleplus.text_table import table


class Job(object):
    _cron_str = ""
    _func = None
    _callback_message = None
    _id = None

    def __init__(self, job_id, cron_str, now=None) -> None:
        self._id = job_id
        self._cron_str = cron_str
        self._cron_parser = CronParser(self._cron_str, now=now)

    def do_function(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def do_callback(self, message: dict):
        self._callback_message = message

    def run_job_meta(self, callback):
        if (
            self._callback_message
            and self._cron_parser.next_run_time() <= datetime.datetime.now()
        ):
            self._cron_parser.iter()
            callback(self._callback_message)

    def run_job_func(self):
        if self._func and self._cron_parser.next_run_time() <= datetime.datetime.now():
            self._cron_parser.iter()
            self._func(*self._args, **self._kwargs)

    def next_run(self):
        return self._cron_parser.next_run_time()

    def time_left(self):
        return str(self._cron_parser.next_run_time() - datetime.datetime.now()).split(
            "."
        )[0]

    def func_name(self):
        if self._func:
            func_name = self._func.__name__
            args = str(self._args).replace("(", "").replace(")", "")
            kwargs = (
                str(self._kwargs)
                .replace("{", "")
                .replace("}", "")
                .replace(": ", "=")
                .replace("'", "")
            )
            if kwargs:
                args += ", "
            return func_name + "(" + args + kwargs + ")"
        return ""

    def cron_str(self):
        return self._cron_str

    def callback_message(self):
        return self._callback_message if self._callback_message else ""

    def id(self):
        return self._id


class Scheduler(object):
    _jobs = []
    _next_job_id = 1

    def __init__(self):
        pass

    def cron(self, cron_str, now=None):
        job_id = self._next_job_id
        self._next_job_id += 1
        job = Job(job_id, cron_str, now)
        self._jobs.append(job)
        self._jobs.sort(key=lambda a: a.next_run())
        return job

    def run_function_jobs(self):
        for job in self._jobs:
            job.run_job_func()

    def run_callback_jobs(self, callback):
        for job in self._jobs:
            job.run_job_meta(callback)

    def dict(self):
        data = {
            "columns": [
                "Job id",
                "Cron",
                "Next run time",
                "Time left",
                "Function",
                "Callback message",
            ],
            "data": [],
        }
        for job in self._jobs:
            data["data"].append(
                (
                    str(job.id()),
                    str(job.cron_str()),
                    str(job.next_run()),
                    str(job.time_left()),
                    str(job.func_name()),
                    str(job.callback_message()),
                )
            )
        return data

    def json(self):
        return json.dumps(self.dict())

    def list_jobs(self):
        data = self.dict()
        print(table(data["columns"], data["data"]))
