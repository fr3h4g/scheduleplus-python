from invoke import task


@task
def lint(c):
    c.run("flake8 src/scheduleplus tests")
    c.run("black src/scheduleplus tests --check")


@task
def test(c):
    c.run("pytest --cov=scheduleplus  --cov=tests --cov-report=xml tests")
