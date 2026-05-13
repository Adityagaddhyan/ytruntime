from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ytruntime.exporters import write_csv_report, write_json_report
from ytruntime.models import PlaylistStats, VideoMetadata
from ytruntime.services import PlaylistService
from ytruntime.services.playlist import (
    EmptyPlaylistError,
    InvalidPlaylistUrlError,
    PlaylistFetchError,
)
from ytruntime.utils import (
    adjusted_duration_seconds,
    format_duration,
    format_speed,
    normalize_speeds,
)

console = Console()
error_console = Console(stderr=True)

PlaylistUrlArg = Annotated[str, typer.Argument(help="YouTube playlist URL.")]
StartOption = Annotated[int | None, typer.Option("--start", help="1-based start index.")]
EndOption = Annotated[int | None, typer.Option("--end", help="1-based end index, inclusive.")]
SpeedOption = Annotated[
    list[float] | None,
    typer.Option(
        "--speed",
        min=0.1,
        help="Additional playback speed to include. Can be used multiple times.",
    ),
]


class ExportFormat(StrEnum):
    csv = "csv"
    json = "json"


def load_stats(playlist_url: str, start: int | None, end: int | None) -> PlaylistStats:
    service = PlaylistService()
    try:
        with console.status("[bold cyan]Fetching playlist metadata...[/]", spinner="dots"):
            return service.fetch_stats(playlist_url, start=start, end=end)
    except KeyboardInterrupt as exc:
        print_warning("Interrupted. No playlist data was changed.")
        raise typer.Exit(code=130) from exc
    except (InvalidPlaylistUrlError, EmptyPlaylistError, PlaylistFetchError, ValueError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc


def render_summary(stats: PlaylistStats, *, speeds: list[float] | None = None) -> None:
    lines = [
        f"[bold]Videos Selected[/] : {stats.total_videos}",
        f"[bold]Total Runtime[/]   : {format_duration(stats.total_seconds)}",
        f"[bold]Average Runtime[/] : {format_duration(stats.average_seconds)}",
    ]
    if stats.playlist_title:
        lines.insert(0, f"[bold]Playlist[/]        : {stats.playlist_title}")

    console.print(
        Panel.fit(
            "\n".join(lines),
            title="[bold]Playlist Statistics[/]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    if stats.skipped_count:
        print_warning(f"Skipped {stats.skipped_count} unavailable or duration-less video(s).")

    render_speed_table(stats, speeds=speeds)


def render_speed_table(stats: PlaylistStats, *, speeds: list[float] | None = None) -> None:
    table = Table(title="Playback Speeds", show_lines=False, header_style="bold magenta")
    table.add_column("Speed", style="magenta", no_wrap=True)
    table.add_column("Total Runtime", style="green", no_wrap=True)
    table.add_column("Average Runtime", style="cyan", no_wrap=True)

    for speed in normalize_speeds(speeds):
        table.add_row(
            format_speed(speed),
            format_duration(adjusted_duration_seconds(stats.total_seconds, speed)),
            format_duration(adjusted_duration_seconds(stats.average_seconds, speed)),
        )

    console.print(table)


def render_video_table(videos: list[VideoMetadata], *, title: str = "Videos") -> None:
    table = Table(title=title, show_lines=False, header_style="bold cyan")
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Duration", style="green", no_wrap=True)
    table.add_column("Title", style="white")

    for video in videos:
        table.add_row(str(video.index), format_duration(video.duration_seconds), video.title)
    console.print(table)


def write_reports(
    stats: PlaylistStats,
    *,
    json_output: Path | None = None,
    csv_output: Path | None = None,
    speeds: list[float] | None = None,
) -> None:
    if json_output is not None:
        write_json_report(stats, json_output, speeds=speeds)
        console.print(f"[green]JSON report written:[/] {json_output}")
    if csv_output is not None:
        write_csv_report(stats, csv_output, speeds=speeds)
        console.print(f"[green]CSV report written:[/] {csv_output}")


def print_error(message: str) -> None:
    error_console.print(
        Panel(
            message,
            title="[bold red]Error[/]",
            border_style="red",
            padding=(1, 2),
        )
    )


def print_warning(message: str) -> None:
    console.print(
        Panel(
            message,
            title="[bold yellow]Warning[/]",
            border_style="yellow",
            padding=(0, 2),
        )
    )
