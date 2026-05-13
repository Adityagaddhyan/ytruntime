from __future__ import annotations

from typer.testing import CliRunner

from ytruntime.cli import app
from ytruntime.models import PlaylistStats, VideoMetadata

runner = CliRunner()


class FakePlaylistService:
    def fetch_stats(
        self,
        playlist_url: str,
        *,
        start: int | None = None,
        end: int | None = None,
    ) -> PlaylistStats:
        assert playlist_url == "https://www.youtube.com/playlist?list=abc"
        assert start == 1
        assert end == 2
        return PlaylistStats(
            videos=[
                VideoMetadata(index=1, title="Intro", duration_seconds=61),
                VideoMetadata(index=2, title="Deep Dive", duration_seconds=120),
            ],
            playlist_title="Course",
        )


def test_version_command() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert "ytruntime" in result.output


def test_stats_command_renders_summary(monkeypatch) -> None:
    monkeypatch.setattr("ytruntime.commands.shared.PlaylistService", FakePlaylistService)

    result = runner.invoke(
        app,
        [
            "stats",
            "https://www.youtube.com/playlist?list=abc",
            "--start",
            "1",
            "--end",
            "2",
        ],
    )

    assert result.exit_code == 0
    assert "Playlist Statistics" in result.output
    assert "Playback Speeds" in result.output
    assert "1.25x" in result.output
    assert "Course" in result.output
    assert "Intro" in result.output


def test_stats_command_accepts_custom_speed(monkeypatch) -> None:
    monkeypatch.setattr("ytruntime.commands.shared.PlaylistService", FakePlaylistService)

    result = runner.invoke(
        app,
        [
            "stats",
            "https://www.youtube.com/playlist?list=abc",
            "--start",
            "1",
            "--end",
            "2",
            "--speed",
            "1.5",
        ],
    )

    assert result.exit_code == 0
    assert "1.5x" in result.output


def test_invalid_url_renders_error_panel() -> None:
    result = runner.invoke(app, ["stats", "https://example.com/not-youtube"])

    assert result.exit_code == 1
    assert "Error" in result.output
    assert "Expected a YouTube playlist URL" in result.output
