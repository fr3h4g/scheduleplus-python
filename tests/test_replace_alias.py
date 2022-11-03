from scheduleplus.cronparser import CronParser


def _run_test(cron_str):
    return CronParser(cron_str)._replace_alias()


def test_replace_alias():
    assert _run_test("@yearly") == "0 0 1 1 *"
    assert _run_test("@annually") == "0 0 1 1 *"
    assert _run_test("@monthly") == "0 0 1 * *"
    assert _run_test("@weekly") == "0 0 * * 0"
    assert _run_test("@daily") == "0 0 * * *"
    assert _run_test("@hourly") == "0 * * * *"
