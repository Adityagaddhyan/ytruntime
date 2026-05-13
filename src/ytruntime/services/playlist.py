from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import parse_qs, urlparse

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError

from ytruntime.models import PlaylistStats, VideoMetadata
from ytruntime.utils import parse_duration


class PlaylistError(RuntimeError):
    """Base error for playlist extraction failures."""


class InvalidPlaylistUrlError(PlaylistError):
    """Raised when a URL does not look like a YouTube playlist URL."""


class EmptyPlaylistError(PlaylistError):
    """Raised when no usable videos are available in the selected range."""


class PlaylistFetchError(PlaylistError):
    """Raised when playlist metadata cannot be fetched."""


class PlaylistService:
    """Fetch and transform YouTube playlist metadata."""

    def fetch_stats(
        self,
        playlist_url: str,
        *,
        start: int | None = None,
        end: int | None = None,
    ) -> PlaylistStats:
        self._validate_url(playlist_url)
        self._validate_range(start, end)

        metadata = self._extract_metadata(playlist_url)
        entries = list(metadata.get("entries") or [])
        if start is not None or end is not None:
            lower = (start or 1) - 1
            upper = end if end is not None else None
            entries = entries[lower:upper]

        videos: list[VideoMetadata] = []
        skipped_count = 0
        for offset, entry in enumerate(entries, start=start or 1):
            if not isinstance(entry, Mapping):
                skipped_count += 1
                continue

            video = self._entry_to_video(entry, offset)
            if video is None:
                skipped_count += 1
                continue
            videos.append(video)

        if not videos:
            raise EmptyPlaylistError("No available videos with durations were found.")

        title = metadata.get("title")
        return PlaylistStats(
            videos=videos,
            skipped_count=skipped_count,
            playlist_title=str(title) if title else None,
        )

    def _extract_metadata(self, playlist_url: str) -> Mapping[str, Any]:
        options: dict[str, Any] = {
            "extract_flat": "in_playlist",
            "ignoreerrors": True,
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }

        try:
            with YoutubeDL(options) as ydl:
                metadata = ydl.extract_info(playlist_url, download=False)
        except (DownloadError, ExtractorError, OSError) as exc:
            raise PlaylistFetchError(f"Failed to fetch playlist metadata: {exc}") from exc

        if not isinstance(metadata, Mapping):
            raise PlaylistFetchError("yt-dlp did not return playlist metadata.")
        if "entries" not in metadata:
            raise InvalidPlaylistUrlError("The URL did not resolve to a playlist.")
        return metadata

    @staticmethod
    def _entry_to_video(entry: Mapping[str, Any], index: int) -> VideoMetadata | None:
        duration = parse_duration(entry.get("duration")) or parse_duration(
            entry.get("duration_string")
        )
        title = entry.get("title")
        if duration is None or not title:
            return None

        webpage_url = entry.get("webpage_url") or entry.get("url")
        return VideoMetadata(
            index=index,
            title=str(title),
            duration_seconds=duration,
            url=str(webpage_url) if webpage_url else None,
        )

    @staticmethod
    def _validate_range(start: int | None, end: int | None) -> None:
        if start is not None and start < 1:
            raise ValueError("--start must be greater than or equal to 1.")
        if end is not None and end < 1:
            raise ValueError("--end must be greater than or equal to 1.")
        if start is not None and end is not None and start > end:
            raise ValueError("--start cannot be greater than --end.")

    @staticmethod
    def _validate_url(playlist_url: str) -> None:
        parsed = urlparse(playlist_url)
        host = parsed.netloc.lower()
        is_youtube = host.endswith("youtube.com") or host.endswith("youtu.be")
        query = parse_qs(parsed.query)
        if parsed.scheme not in {"http", "https"} or not is_youtube or "list" not in query:
            raise InvalidPlaylistUrlError(
                "Expected a YouTube playlist URL containing a list parameter."
            )
