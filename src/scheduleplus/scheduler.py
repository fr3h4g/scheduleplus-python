import json

from workalendar.europe import Sweden

from scheduleplus.text_table import table
from scheduleplus.job import Job


class Scheduler(object):
    _jobs = []
    _next_job_id = 1

    def __init__(self):
        pass

    def cron(self, cron_str, now=None, wk_country=None):
        if not wk_country:
            wk_country = Sweden
        self._wk_country = wk_country
        job_id = self._next_job_id
        self._next_job_id += 1
        job = Job(job_id, cron_str, now, wk_country)
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
