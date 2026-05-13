from __future__ import annotations

from typing import Annotated

import typer

from ytruntime import __version__
from ytruntime.commands import register_export, register_rankings, register_stats

app = typer.Typer(
    name="ytruntime",
    help="Calculate YouTube playlist runtime statistics.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"ytruntime {__version__}")
        raise typer.Exit


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            help="Show the installed ytruntime version and exit.",
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Calculate YouTube playlist runtime statistics."""


register_stats(app)
register_export(app)
register_rankings(app)
