from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from ytruntime.commands.shared import (
    EndOption,
    PlaylistUrlArg,
    StartOption,
    load_stats,
    render_summary,
    render_video_table,
    write_reports,
)


def register(app: typer.Typer) -> None:
    app.command(name="stats")(stats)


def stats(
    playlist_url: PlaylistUrlArg,
    start: StartOption = None,
    end: EndOption = None,
    json_output: Annotated[
        Path | None,
        typer.Option("--json", help="Write a JSON report to this path."),
    ] = None,
    csv_output: Annotated[
        Path | None,
        typer.Option("--csv", help="Write a CSV report to this path."),
    ] = None,
) -> None:
    """Print playlist runtime statistics."""
    playlist_stats = load_stats(playlist_url, start, end)
    render_summary(playlist_stats)
    render_video_table(playlist_stats.videos)
    write_reports(playlist_stats, json_output=json_output, csv_output=csv_output)
