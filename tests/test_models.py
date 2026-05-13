from ytruntime.models import PlaylistStats, VideoMetadata


def test_playlist_stats_calculations() -> None:
    stats = PlaylistStats(
        videos=[
            VideoMetadata(index=1, title="One", duration_seconds=60),
            VideoMetadata(index=2, title="Two", duration_seconds=120),
            VideoMetadata(index=3, title="Three", duration_seconds=121),
        ]
    )

    assert stats.total_videos == 3
    assert stats.total_seconds == 301
    assert stats.average_seconds == 100


def test_empty_playlist_stats_average_is_zero() -> None:
    stats = PlaylistStats(videos=[])

    assert stats.total_videos == 0
    assert stats.total_seconds == 0
    assert stats.average_seconds == 0
