from scheduleplus.util import parse_minute


def test_parse_minute():
    assert parse_minute("*") == [item for item in range(0, 60)]
    assert parse_minute("*/2") == [item for item in range(0, 60, 2)]
    assert parse_minute("1-10/2") == [item for item in range(1, 11, 2)]
    assert parse_minute("1/2") == [item for item in range(1, 60, 2)]
    assert parse_minute("10-20/9") == [10, 19]
    assert parse_minute("10-10/9") == [10]
    assert parse_minute("10,59") == [10, 59]
    assert parse_minute("1,2,3,4,5,10,11,12,13") == [1, 2, 3, 4, 5, 10, 11, 12, 13]
    assert parse_minute("10-10,20-30/2") == [10, 20, 22, 24, 26, 28, 30]
    assert parse_minute("55/2") == [55, 57, 59]
    assert parse_minute("40,55") == [40, 55]
    assert parse_minute("40,55,40,55") == [40, 55]
    assert parse_minute("55,40") == [40, 55]
    assert parse_minute("0-5/2,10-12,20,22") == [0, 2, 4, 10, 11, 12, 20, 22]
