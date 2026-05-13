from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ytruntime.models import PlaylistStats, VideoMetadata
from ytruntime.services import PlaylistService, write_csv_report, write_json_report
from ytruntime.services.playlist import (
    EmptyPlaylistError,
    InvalidPlaylistUrlError,
    PlaylistFetchError,
)
from ytruntime.utils import format_duration

app = typer.Typer(
    name="ytruntime",
    help="Calculate YouTube playlist runtime statistics.",
    no_args_is_help=True,
)
console = Console()
error_console = Console(stderr=True)


class ExportFormat(StrEnum):
    csv = "csv"
    json = "json"


PlaylistUrlArg = Annotated[str, typer.Argument(help="YouTube playlist URL.")]
StartOption = Annotated[int | None, typer.Option("--start", help="1-based start index.")]
EndOption = Annotated[int | None, typer.Option("--end", help="1-based end index, inclusive.")]


def _load_stats(playlist_url: str, start: int | None, end: int | None) -> PlaylistStats:
    service = PlaylistService()
    try:
        with console.status("[bold cyan]Fetching playlist metadata...[/]", spinner="dots"):
            return service.fetch_stats(playlist_url, start=start, end=end)
    except (InvalidPlaylistUrlError, EmptyPlaylistError, PlaylistFetchError, ValueError) as exc:
        error_console.print(f"[bold red]Error:[/] {exc}")
        raise typer.Exit(code=1) from exc


def _render_summary(stats: PlaylistStats) -> None:
    lines = [
        f"[bold]Videos Selected[/] : {stats.total_videos}",
        f"[bold]Total Runtime[/]   : {format_duration(stats.total_seconds)}",
        f"[bold]Average Runtime[/] : {format_duration(stats.average_seconds)}",
    ]
    if stats.skipped_count:
        lines.append(f"[bold yellow]Videos Skipped[/]  : {stats.skipped_count}")
    if stats.playlist_title:
        lines.insert(0, f"[bold]Playlist[/]        : {stats.playlist_title}")

    console.print(
        Panel.fit(
            "\n".join(lines),
            title="[bold]Playlist Statistics[/]",
            border_style="cyan",
        )
    )


def _render_video_table(videos: list[VideoMetadata], *, title: str = "Videos") -> None:
    table = Table(title=title, show_lines=False)
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Duration", style="green", no_wrap=True)
    table.add_column("Title", style="white")

    for video in videos:
        table.add_row(str(video.index), format_duration(video.duration_seconds), video.title)
    console.print(table)


def _write_reports(
    stats: PlaylistStats,
    *,
    json_output: Path | None = None,
    csv_output: Path | None = None,
) -> None:
    if json_output is not None:
        write_json_report(stats, json_output)
        console.print(f"[green]JSON report written:[/] {json_output}")
    if csv_output is not None:
        write_csv_report(stats, csv_output)
        console.print(f"[green]CSV report written:[/] {csv_output}")


@app.command()
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
    playlist_stats = _load_stats(playlist_url, start, end)
    _render_summary(playlist_stats)
    _render_video_table(playlist_stats.videos)
    _write_reports(playlist_stats, json_output=json_output, csv_output=csv_output)


@app.command()
def export(
    playlist_url: PlaylistUrlArg,
    output: Annotated[Path, typer.Option("--output", "-o", help="Report output path.")],
    report_format: Annotated[
        ExportFormat,
        typer.Option("--format", "-f", help="Report format."),
    ] = ExportFormat.json,
    start: StartOption = None,
    end: EndOption = None,
) -> None:
    """Export playlist statistics without printing the full video table."""
    playlist_stats = _load_stats(playlist_url, start, end)
    if report_format is ExportFormat.json:
        write_json_report(playlist_stats, output)
    else:
        write_csv_report(playlist_stats, output)
    console.print(f"[green]{report_format.value.upper()} report written:[/] {output}")


@app.command()
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
    playlist_stats = _load_stats(playlist_url, start, end)
    videos = sorted(
        playlist_stats.videos,
        key=lambda video: video.duration_seconds,
        reverse=True,
    )[:limit]
    _render_video_table(videos, title="Longest Videos")


@app.command()
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
    playlist_stats = _load_stats(playlist_url, start, end)
    videos = sorted(playlist_stats.videos, key=lambda video: video.duration_seconds)[:limit]
    _render_video_table(videos, title="Shortest Videos")
