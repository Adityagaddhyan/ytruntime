import pytest

from ytruntime.utils import (
    adjusted_duration_seconds,
    format_duration,
    format_speed,
    normalize_speeds,
    parse_duration,
)


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "0s"),
        (7, "7s"),
        (61, "1m 01s"),
        (3600, "1h 0m 00s"),
        (3723, "1h 2m 03s"),
    ],
)
def test_format_duration(seconds: int, expected: str) -> None:
    assert format_duration(seconds) == expected


def test_format_duration_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="negative"):
        format_duration(-1)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (90, 90),
        ("90", 90),
        ("1:30", 90),
        ("01:02:03", 3723),
        ("1h 2m 3s", 3723),
        ("unavailable", None),
        (0, None),
    ],
)
def test_parse_duration(value: object, expected: int | None) -> None:
    assert parse_duration(value) == expected


def test_default_playback_speeds_include_expected_values() -> None:
    assert normalize_speeds() == [1.0, 1.25, 1.75, 2.0]


def test_custom_playback_speed_is_added() -> None:
    assert normalize_speeds([1.5, 1.25]) == [1.0, 1.25, 1.5, 1.75, 2.0]


def test_adjusted_duration_seconds() -> None:
    assert adjusted_duration_seconds(120, 1.0) == 120
    assert adjusted_duration_seconds(120, 1.5) == 80


def test_format_speed() -> None:
    assert format_speed(1.0) == "1x"
    assert format_speed(1.25) == "1.25x"
