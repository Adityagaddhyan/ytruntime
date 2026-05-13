import re


def format_duration(total_seconds: int) -> str:
    """Format seconds as a compact human-readable duration."""
    if total_seconds < 0:
        raise ValueError("Duration cannot be negative")

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts: list[str] = []
    if hours:
        parts.append(f"{hours}h")
    if minutes or hours:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds:02d}s" if minutes or hours else f"{seconds}s")
    return " ".join(parts)


def parse_duration(value: object) -> int | None:
    """Parse yt-dlp duration values into seconds when possible."""
    if isinstance(value, int) and value > 0:
        return value
    if not isinstance(value, str):
        return None

    value = value.strip()
    if not value:
        return None

    if value.isdigit():
        seconds = int(value)
        return seconds if seconds > 0 else None

    colon_parts = value.split(":")
    if all(part.isdigit() for part in colon_parts) and 1 < len(colon_parts) <= 3:
        seconds = 0
        for part in colon_parts:
            seconds = seconds * 60 + int(part)
        return seconds if seconds > 0 else None

    matches = re.findall(r"(\d+)\s*([hms])", value.lower())
    if not matches:
        return None

    multipliers = {"h": 3600, "m": 60, "s": 1}
    seconds = sum(int(number) * multipliers[unit] for number, unit in matches)
    return seconds if seconds > 0 else None
