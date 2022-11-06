import datetime

from workalendar.europe import Sweden

from scheduleplus.cronparser import CronParser


class Job(object):
    _cron_str = ""
    _func = None
    _callback_message = None
    _id = None

    def __init__(self, job_id, cron_str, now=None, wk_country=None) -> None:
        if not wk_country:
            wk_country = Sweden
        self._id = job_id
        self._wk_country = wk_country
        self._cron_str = cron_str
        self._cron_parser = CronParser(self._cron_str, now=now, wk_country=wk_country)

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
