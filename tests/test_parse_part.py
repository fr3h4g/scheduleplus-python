from scheduleplus.cronparser import CronParser


def _run_test(part_str, part):
    return CronParser("* * * * *")._parse_part(part_str, part)


def test_parse_minute():
    part = 0
    assert _run_test("*", part) == [item for item in range(0, 60)]
    assert _run_test("*/2", part) == [item for item in range(0, 60, 2)]
    assert _run_test("*/30", part) == [0, 30]
    assert _run_test("1-10/2", part) == [item for item in range(1, 11, 2)]
    assert _run_test("1/2", part) == [item for item in range(1, 60, 2)]
    assert _run_test("10-20/9", part) == [10, 19]
    assert _run_test("10-10/9", part) == [10]
    assert _run_test("10,59", part) == [10, 59]
    assert _run_test("1,2,3,4,5,10,11,12,13", part) == [1, 2, 3, 4, 5, 10, 11, 12, 13]
    assert _run_test("10-10,20-30/2", part) == [10, 20, 22, 24, 26, 28, 30]
    assert _run_test("55/2", part) == [55, 57, 59]
    assert _run_test("40,55", part) == [40, 55]
    assert _run_test("40,55,40,55", part) == [40, 55]
    assert _run_test("55,40", part) == [40, 55]
    assert _run_test("0-5/2,10-12,20,22", part) == [0, 2, 4, 10, 11, 12, 20, 22]
    assert _run_test("100", part) == []


def test_parse_hour():
    part = 1
    assert _run_test("*", part) == [item for item in range(0, 24)]
    assert _run_test("24", part) == []
    assert _run_test("23", part) == [23]


def test_parse_day():
    part = 2
    assert _run_test("*", part) == [item for item in range(1, 32)]
    assert _run_test("32", part) == []
    assert _run_test("31", part) == [31]


def test_parse_month():
    part = 3
    assert _run_test("*", part) == [item for item in range(1, 13)]
    assert _run_test("13", part) == []
    assert _run_test("12", part) == [12]
    assert _run_test("DeC", part) == [12]
    assert _run_test("JaN/1", part) == [item for item in range(1, 13)]


def test_parse_weekday():
    part = 4
    assert _run_test("*", part) == [item for item in range(0, 7)]
    assert _run_test("7", part) == []
    assert _run_test("6", part) == [6]
    assert _run_test("MoN-tUe", part) == [0, 1]
    assert _run_test("MoN-fRi/2", part) == [0, 2, 4]
    assert _run_test("MoN-fRi/10", part) == [0]
