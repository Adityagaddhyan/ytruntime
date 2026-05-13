from __future__ import annotations

DEFAULT_PLAYBACK_SPEEDS: tuple[float, ...] = (1.0, 1.25, 1.75, 2.0)


def adjusted_duration_seconds(duration_seconds: int, speed: float) -> int:
    if speed <= 0:
        raise ValueError("Playback speed must be greater than 0.")
    return round(duration_seconds / speed)


def normalize_speeds(custom_speeds: list[float] | None = None) -> list[float]:
    speeds = [*DEFAULT_PLAYBACK_SPEEDS, *(custom_speeds or [])]
    return sorted(set(speeds))


def format_speed(speed: float) -> str:
    return f"{speed:g}x"
