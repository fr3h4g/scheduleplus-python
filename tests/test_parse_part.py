from scheduleplus.util import _parse_part


def test_parse_minute():
    part = 0
    assert _parse_part("*", part) == [item for item in range(0, 60)]
    assert _parse_part("*/2", part) == [item for item in range(0, 60, 2)]
    assert _parse_part("*/30", part) == [0, 30]
    assert _parse_part("1-10/2", part) == [item for item in range(1, 11, 2)]
    assert _parse_part("1/2", part) == [item for item in range(1, 60, 2)]
    assert _parse_part("10-20/9", part) == [10, 19]
    assert _parse_part("10-10/9", part) == [10]
    assert _parse_part("10,59", part) == [10, 59]
    assert _parse_part("1,2,3,4,5,10,11,12,13", part) == [1, 2, 3, 4, 5, 10, 11, 12, 13]
    assert _parse_part("10-10,20-30/2", part) == [10, 20, 22, 24, 26, 28, 30]
    assert _parse_part("55/2", part) == [55, 57, 59]
    assert _parse_part("40,55", part) == [40, 55]
    assert _parse_part("40,55,40,55", part) == [40, 55]
    assert _parse_part("55,40", part) == [40, 55]
    assert _parse_part("0-5/2,10-12,20,22", part) == [0, 2, 4, 10, 11, 12, 20, 22]
    assert _parse_part("100", part) == []


def test_parse_hour():
    part = 1
    assert _parse_part("*", part) == [item for item in range(0, 24)]
    assert _parse_part("24", part) == []
    assert _parse_part("23", part) == [23]


def test_parse_day():
    part = 2
    assert _parse_part("*", part) == [item for item in range(1, 32)]
    assert _parse_part("32", part) == []
    assert _parse_part("31", part) == [31]


def test_parse_month():
    part = 3
    assert _parse_part("*", part) == [item for item in range(1, 13)]
    assert _parse_part("13", part) == []
    assert _parse_part("12", part) == [12]
    assert _parse_part("DeC", part) == [12]
    assert _parse_part("JaN/1", part) == [item for item in range(1, 13)]


def test_parse_weekday():
    part = 4
    assert _parse_part("*", part) == [item for item in range(0, 7)]
    assert _parse_part("7", part) == []
    assert _parse_part("6", part) == [6]
    assert _parse_part("MoN-tUe", part) == [1, 2]
    assert _parse_part("MoN-fRi/2", part) == [1, 3, 5]
    assert _parse_part("MoN-fRi/10", part) == [1]
