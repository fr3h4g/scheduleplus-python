from scheduleplus.text_table import table


def test_text_table():
    cols = ("c1", "c2")
    data = [("d1", "d_2", "d_2")]
    table(cols, data)
