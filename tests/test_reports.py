import json

from ytruntime.models import PlaylistStats, VideoMetadata
from ytruntime.services.reports import stats_to_dict, write_csv_report, write_json_report


def test_stats_to_dict() -> None:
    stats = PlaylistStats(
        videos=[
            VideoMetadata(index=1, title="Intro", duration_seconds=61, url="https://example.com/1"),
            VideoMetadata(index=2, title="Deep Dive", duration_seconds=120),
        ],
        skipped_count=1,
        playlist_title="Course",
    )

    payload = stats_to_dict(stats)

    assert payload["playlist_title"] == "Course"
    assert payload["videos_selected"] == 2
    assert payload["skipped_count"] == 1
    assert payload["total_seconds"] == 181
    assert payload["average_seconds"] == 90
    assert payload["videos"][0]["duration"] == "1m 01s"


def test_write_reports(tmp_path) -> None:
    stats = PlaylistStats(videos=[VideoMetadata(index=1, title="Intro", duration_seconds=61)])
    json_path = tmp_path / "report.json"
    csv_path = tmp_path / "report.csv"

    write_json_report(stats, json_path)
    write_csv_report(stats, csv_path)

    assert json.loads(json_path.read_text(encoding="utf-8"))["videos_selected"] == 1
    assert "index,duration_seconds,duration,title,url" in csv_path.read_text(encoding="utf-8")
