from scheduleplus.util import _replace_alias


def test_replace_alias():
    assert _replace_alias("@daily") == "0 0 * * *"
