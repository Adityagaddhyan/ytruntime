# ytruntime

## TL;DR

```bash
uv tool install git+https://github.com/Adityagaddhyan/ytruntime.git
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

`ytruntime` is a Python CLI that calculates runtime statistics for YouTube
playlists. It prints the total video count, total runtime, average runtime, and
per-video durations with titles.

## Install

Requires Python 3.11+.

Install directly from GitHub:

```bash
uv tool install git+https://github.com/Adityagaddhyan/ytruntime.git
```

Or with `pipx`:

```bash
pipx install git+https://github.com/Adityagaddhyan/ytruntime.git
```

After publishing to PyPI, users can install it by package name:

```bash
uv tool install ytruntime
pipx install ytruntime
pip install ytruntime
```

All install methods expose the executable:

```bash
ytruntime
```

Homebrew support should live in a tap, for example:

```bash
brew tap Adityagaddhyan/tap
brew install ytruntime
```

That requires publishing a Homebrew formula in `Adityagaddhyan/homebrew-tap`
after a tagged release is available.

## Usage

Print playlist stats:

```bash
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

Select an inclusive 1-based range:

```bash
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID" --start 5 --end 20
```

Export reports:

```bash
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID" --json report.json
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID" --csv report.csv
```

Dedicated export command:

```bash
ytruntime export "https://www.youtube.com/playlist?list=PLAYLIST_ID" --format json --output report.json
ytruntime export "https://www.youtube.com/playlist?list=PLAYLIST_ID" --format csv --output report.csv
```

Find longest or shortest videos:

```bash
ytruntime longest "https://www.youtube.com/playlist?list=PLAYLIST_ID" --limit 10
ytruntime shortest "https://www.youtube.com/playlist?list=PLAYLIST_ID" --limit 10
```

## Commands

- `stats`: print playlist runtime statistics.
- `export`: write JSON or CSV output.
- `longest`: show the longest videos.
- `shortest`: show the shortest videos.

## Development

```bash
uv sync --extra dev
uv run ytruntime --help
uv run pytest
uv run ruff check .
```
