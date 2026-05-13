from __future__ import annotations

from typing import Annotated

import typer

from ytruntime.commands.shared import (
    EndOption,
    PlaylistUrlArg,
    StartOption,
    load_stats,
    render_video_table,
)
from ytruntime.models import VideoMetadata


def register(app: typer.Typer) -> None:
    app.command(name="longest")(longest)
    app.command(name="shortest")(shortest)


def longest(
    playlist_url: PlaylistUrlArg,
    limit: Annotated[
        int,
        typer.Option("--limit", "-n", min=1, help="Number of videos to show."),
    ] = 10,
    start: StartOption = None,
    end: EndOption = None,
) -> None:
    """Show the longest videos in a playlist."""
    playlist_stats = load_stats(playlist_url, start, end)
    videos = _rank_videos(playlist_stats.videos, limit=limit, reverse=True)
    render_video_table(videos, title="Longest Videos")


def shortest(
    playlist_url: PlaylistUrlArg,
    limit: Annotated[
        int,
        typer.Option("--limit", "-n", min=1, help="Number of videos to show."),
    ] = 10,
    start: StartOption = None,
    end: EndOption = None,
) -> None:
    """Show the shortest videos in a playlist."""
    playlist_stats = load_stats(playlist_url, start, end)
    videos = _rank_videos(playlist_stats.videos, limit=limit, reverse=False)
    render_video_table(videos, title="Shortest Videos")


def _rank_videos(
    videos: list[VideoMetadata],
    *,
    limit: int,
    reverse: bool,
) -> list[VideoMetadata]:
    return sorted(videos, key=lambda video: video.duration_seconds, reverse=reverse)[:limit]
