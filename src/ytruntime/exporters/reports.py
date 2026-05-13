from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from ytruntime.models import PlaylistStats
from ytruntime.utils import (
    adjusted_duration_seconds,
    format_duration,
    format_speed,
    normalize_speeds,
)


def stats_to_dict(stats: PlaylistStats, *, speeds: list[float] | None = None) -> dict[str, Any]:
    normalized_speeds = normalize_speeds(speeds)
    return {
        "playlist_title": stats.playlist_title,
        "videos_selected": stats.total_videos,
        "skipped_count": stats.skipped_count,
        "total_seconds": stats.total_seconds,
        "total_runtime": format_duration(stats.total_seconds),
        "average_seconds": stats.average_seconds,
        "average_runtime": format_duration(stats.average_seconds),
        "playback_speeds": [
            {
                "speed": speed,
                "label": format_speed(speed),
                "total_seconds": adjusted_duration_seconds(stats.total_seconds, speed),
                "total_runtime": format_duration(
                    adjusted_duration_seconds(stats.total_seconds, speed)
                ),
                "average_seconds": adjusted_duration_seconds(stats.average_seconds, speed),
                "average_runtime": format_duration(
                    adjusted_duration_seconds(stats.average_seconds, speed)
                ),
            }
            for speed in normalized_speeds
        ],
        "videos": [
            {
                "index": video.index,
                "title": video.title,
                "duration_seconds": video.duration_seconds,
                "duration": format_duration(video.duration_seconds),
                "url": video.url,
            }
            for video in stats.videos
        ],
    }


def write_json_report(
    stats: PlaylistStats,
    output_path: Path,
    *,
    speeds: list[float] | None = None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(stats_to_dict(stats, speeds=speeds), indent=2) + "\n",
        encoding="utf-8",
    )


def write_csv_report(
    stats: PlaylistStats,
    output_path: Path,
    *,
    speeds: list[float] | None = None,
) -> None:
    normalized_speeds = normalize_speeds(speeds)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        speed_fields = [f"duration_{format_speed(speed)}" for speed in normalized_speeds]
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "index",
                "duration_seconds",
                "duration",
                *speed_fields,
                "title",
                "url",
            ],
        )
        writer.writeheader()
        for video in stats.videos:
            speed_values = {
                f"duration_{format_speed(speed)}": format_duration(
                    adjusted_duration_seconds(video.duration_seconds, speed)
                )
                for speed in normalized_speeds
            }
            writer.writerow(
                {
                    "index": video.index,
                    "duration_seconds": video.duration_seconds,
                    "duration": format_duration(video.duration_seconds),
                    **speed_values,
                    "title": video.title,
                    "url": video.url or "",
                }
            )
