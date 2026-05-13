import pytest

from ytruntime.utils import format_duration, parse_duration


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
