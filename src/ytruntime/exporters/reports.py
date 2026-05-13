from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from ytruntime.models import PlaylistStats
from ytruntime.utils import format_duration


def stats_to_dict(stats: PlaylistStats) -> dict[str, Any]:
    return {
        "playlist_title": stats.playlist_title,
        "videos_selected": stats.total_videos,
        "skipped_count": stats.skipped_count,
        "total_seconds": stats.total_seconds,
        "total_runtime": format_duration(stats.total_seconds),
        "average_seconds": stats.average_seconds,
        "average_runtime": format_duration(stats.average_seconds),
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


def write_json_report(stats: PlaylistStats, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(stats_to_dict(stats), indent=2) + "\n", encoding="utf-8")


def write_csv_report(stats: PlaylistStats, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["index", "duration_seconds", "duration", "title", "url"],
        )
        writer.writeheader()
        for video in stats.videos:
            writer.writerow(
                {
                    "index": video.index,
                    "duration_seconds": video.duration_seconds,
                    "duration": format_duration(video.duration_seconds),
                    "title": video.title,
                    "url": video.url or "",
                }
            )
