from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VideoMetadata:
    """Metadata needed for runtime calculations."""

    index: int
    title: str
    duration_seconds: int
    url: str | None = None


@dataclass(frozen=True, slots=True)
class PlaylistStats:
    """Computed statistics for a playlist selection."""

    videos: list[VideoMetadata]
    skipped_count: int = 0
    playlist_title: str | None = None

    @property
    def total_videos(self) -> int:
        return len(self.videos)

    @property
    def total_seconds(self) -> int:
        return sum(video.duration_seconds for video in self.videos)

    @property
    def average_seconds(self) -> int:
        if not self.videos:
            return 0
        return round(self.total_seconds / len(self.videos))
