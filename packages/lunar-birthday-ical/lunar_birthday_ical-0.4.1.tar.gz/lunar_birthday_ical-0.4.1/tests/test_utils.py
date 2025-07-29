from lunar_birthday_ical.utils import deep_merge, deep_merge_iterative


def test_deep_merge():
    d1 = {"a": 1, "b": {"c": 2, "d": 3}}
    d2 = {"b": {"c": 4, "e": 5}, "f": 6}
    expected = {"a": 1, "b": {"c": 4, "d": 3, "e": 5}, "f": 6}
    assert deep_merge(d1, d2) == expected


def test_deep_merge_overwrite():
    d1 = {"a": 1, "b": {"c": 2}}
    d2 = {"a": 2, "b": {"c": 3}}
    expected = {"a": 2, "b": {"c": 3}}
    assert deep_merge(d1, d2) == expected


def test_deep_merge_iterative():
    d1 = {"a": 1, "b": {"c": 2, "d": 3}}
    d2 = {"b": {"c": 4, "e": 5}, "f": 6}
    expected = {"a": 1, "b": {"c": 4, "d": 3, "e": 5}, "f": 6}
    assert deep_merge_iterative(d1, d2) == expected


def test_deep_merge_iterative_overwrite():
    d1 = {"a": 1, "b": {"c": 2}}
    d2 = {"a": 2, "b": {"c": 3}}
    expected = {"a": 2, "b": {"c": 3}}
    assert deep_merge_iterative(d1, d2) == expected


def test_deep_merge_iterative_nested():
    d1 = {"a": 1, "b": {"c": {"d": 2}}}
    d2 = {"b": {"c": {"e": 3}}}
    expected = {"a": 1, "b": {"c": {"d": 2, "e": 3}}}
    assert deep_merge_iterative(d1, d2) == expected
