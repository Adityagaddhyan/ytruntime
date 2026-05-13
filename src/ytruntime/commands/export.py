from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from ytruntime.commands.shared import (
    EndOption,
    ExportFormat,
    PlaylistUrlArg,
    SpeedOption,
    StartOption,
    console,
    load_stats,
)
from ytruntime.exporters import write_csv_report, write_json_report


def register(app: typer.Typer) -> None:
    app.command(name="export")(export)


def export(
    playlist_url: PlaylistUrlArg,
    output: Annotated[Path, typer.Option("--output", "-o", help="Report output path.")],
    report_format: Annotated[
        ExportFormat,
        typer.Option("--format", "-f", help="Report format."),
    ] = ExportFormat.json,
    start: StartOption = None,
    end: EndOption = None,
    speed: SpeedOption = None,
) -> None:
    """Export playlist statistics without printing the full video table."""
    playlist_stats = load_stats(playlist_url, start, end)
    if report_format is ExportFormat.json:
        write_json_report(playlist_stats, output, speeds=speed)
    else:
        write_csv_report(playlist_stats, output, speeds=speed)
    console.print(f"[green]{report_format.value.upper()} report written:[/] {output}")
