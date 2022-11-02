import datetime
from datetime import timedelta


class Job(object):
    _cron_str = ""

    def __init__(self, cron_str) -> None:
        self._cron_str = cron_str

    def do(self, func):
        pass

    def next_run(self, now=None):
        if not now:
            now = datetime.datetime.now()

        return now + timedelta(minutes=5)


class Scheduler(object):
    jobs = []

    def __init__(self):
        pass

    def cron(self, cron_str):
        job = Job(cron_str)
        self.jobs.append(job)
        return job

    def run_jobs(self):
        print("Running...")
