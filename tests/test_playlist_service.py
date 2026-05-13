from typing import Any

import pytest

from ytruntime.services.playlist import EmptyPlaylistError, InvalidPlaylistUrlError, PlaylistService


class FakePlaylistService(PlaylistService):
    def __init__(self, metadata: dict[str, Any]) -> None:
        self.metadata = metadata

    def _extract_metadata(self, playlist_url: str) -> dict[str, Any]:
        return self.metadata


def test_fetch_stats_filters_and_slices_entries() -> None:
    service = FakePlaylistService(
        {
            "title": "Playlist",
            "entries": [
                {"title": "One", "duration": 10, "webpage_url": "https://youtu.be/1"},
                None,
                {"title": "Two", "duration": 20},
                {"title": "No duration"},
                {"title": "Three", "duration": 30},
            ],
        }
    )

    stats = service.fetch_stats("https://www.youtube.com/playlist?list=abc", start=2, end=5)

    assert stats.playlist_title == "Playlist"
    assert stats.skipped_count == 2
    assert [video.index for video in stats.videos] == [3, 5]
    assert stats.total_seconds == 50


def test_invalid_playlist_url_is_rejected() -> None:
    service = FakePlaylistService({"entries": []})

    with pytest.raises(InvalidPlaylistUrlError):
        service.fetch_stats("https://example.com/not-youtube")


def test_invalid_range_is_rejected() -> None:
    service = FakePlaylistService({"entries": []})

    with pytest.raises(ValueError, match="start"):
        service.fetch_stats("https://www.youtube.com/playlist?list=abc", start=10, end=2)


def test_empty_playlist_is_rejected() -> None:
    service = FakePlaylistService({"entries": []})

    with pytest.raises(EmptyPlaylistError):
        service.fetch_stats("https://www.youtube.com/playlist?list=abc")
