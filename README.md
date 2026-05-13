# ytruntime

[![CI](https://github.com/Adityagaddhyan/ytruntime/actions/workflows/ci.yml/badge.svg)](https://github.com/Adityagaddhyan/ytruntime/actions/workflows/ci.yml)
[![PyPI Version](https://img.shields.io/pypi/v/ytruntime)](https://pypi.org/project/ytruntime/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ytruntime)](https://pypi.org/project/ytruntime/)

## TL;DR

```bash
uv tool install git+https://github.com/Adityagaddhyan/ytruntime.git
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

`ytruntime` is a polished Python CLI for calculating YouTube playlist runtimes.
It prints total videos, total runtime, average runtime, and a per-video duration
table. It uses `yt-dlp` for metadata extraction and `rich` for terminal output.

## Why ytruntime?

- Quickly estimate how long a course, lecture series, or watchlist will take.
- Select a playlist range with `--start` and `--end`.
- Skip unavailable/private videos gracefully.
- Export JSON or CSV reports for notes, scripts, and dashboards.
- Install as a real global CLI with `uv tool`, `pipx`, or PyPI.

## Installation

| Method | Command | Status |
| --- | --- | --- |
| `uv tool` from GitHub | `uv tool install git+https://github.com/Adityagaddhyan/ytruntime.git` | Works now |
| `pipx` from GitHub | `pipx install git+https://github.com/Adityagaddhyan/ytruntime.git` | Works now |
| `uv tool` from PyPI | `uv tool install ytruntime` | After PyPI release |
| `pipx` from PyPI | `pipx install ytruntime` | After PyPI release |
| `pip` from PyPI | `pip install ytruntime` | After PyPI release |
| Homebrew | `brew install ytruntime` | Planned |

Requires Python 3.11+.

If `uv tool install` succeeds but `ytruntime` is not found, add uv's tool
directory to your shell:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Or let uv update your shell configuration:

```bash
uv tool update-shell
```

## Usage

Print playlist stats:

```bash
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

Select an inclusive 1-based range:

```bash
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID" --start 5 --end 20
```

Export while printing stats:

```bash
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID" --json report.json
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID" --csv report.csv
```

By default, stats also show playback-adjusted runtimes for `1x`, `1.25x`,
`1.75x`, and `2x`.

Add custom playback speeds:

```bash
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID" --speed 1.5
ytruntime stats "https://www.youtube.com/playlist?list=PLAYLIST_ID" --speed 1.5 --speed 3
```

Use the dedicated export command:

```bash
ytruntime export "https://www.youtube.com/playlist?list=PLAYLIST_ID" --format json --output report.json
ytruntime export "https://www.youtube.com/playlist?list=PLAYLIST_ID" --format csv --output report.csv
```

Find the longest or shortest videos:

```bash
ytruntime longest "https://www.youtube.com/playlist?list=PLAYLIST_ID" --limit 10
ytruntime shortest "https://www.youtube.com/playlist?list=PLAYLIST_ID" --limit 10
```

Check the installed version:

```bash
ytruntime --version
```

## Demo Screenshots

Screenshots should be added after the first tagged release.

Suggested captures:

- `ytruntime stats ...`
- `ytruntime stats ... --json report.json`
- error output for an invalid playlist URL

## Shell Completion

Install shell completion for your current shell:

```bash
ytruntime --install-completion
```

Restart your shell after installation.

## Commands

- `stats`: print playlist runtime statistics.
- `export`: write JSON or CSV output.
- `longest`: show the longest videos.
- `shortest`: show the shortest videos.

## Development

```bash
uv sync --extra dev
uv run ytruntime --help
uv run ruff check .
uv run pytest
uv build
```

Check global install behavior locally:

```bash
pipx install .
uv tool install .
```

## Release

Releases are built by GitHub Actions when a tag like `v0.1.0` is pushed. The
release workflow runs tests, builds the wheel and source distribution, uploads
the artifacts, publishes to PyPI, and creates a GitHub Release with generated
release notes.

Maintainer setup:

1. Create the `ytruntime` project on PyPI.
2. Create a PyPI API token with permission to publish `ytruntime`.
3. Add the token to this GitHub repository as a secret named `PYPI_API_TOKEN`.

Publish a new version:

```bash
uv sync --extra dev --frozen
uv run ruff check .
uv run pytest
uv build
git status
git tag v0.1.0
git push origin main
git push origin v0.1.0
```

Use a new tag for every release. PyPI does not allow replacing an already
published version, so update `version` in `pyproject.toml` before tagging.

## Homebrew Prep

Homebrew support should be added after the first GitHub release exists.

Planned flow:

```bash
brew tap Adityagaddhyan/tap
brew install ytruntime
```

The future tap repo should be named `Adityagaddhyan/homebrew-tap` and contain a
formula that installs the released wheel or source archive from GitHub/PyPI.

## License

MIT
