"""対象尺の選択ロジックのテスト。"""

from common import select_targets


def _rows() -> list[dict[str, object]]:
    return [
        {
            "content_key": "001-none",
            "video_s3_key_20s": None,
            "video_s3_key_30s": None,
        },
        {
            "content_key": "002-partial",
            "video_s3_key_20s": "built-20.mp4",
            "video_s3_key_30s": None,
        },
        {
            "content_key": "003-all",
            "video_s3_key_20s": "built-20.mp4",
            "video_s3_key_30s": "built-30.mp4",
        },
    ]


def test_select_targets_selects_only_unbuilt_durations() -> None:
    targets = select_targets(_rows(), ("20s", "30s"), rebuild=False)

    assert [(item["content_key"], item["target_durations"]) for item in targets] == [
        ("001-none", ["20s", "30s"]),
        ("002-partial", ["30s"]),
    ]


def test_select_targets_rebuilds_only_built_durations() -> None:
    targets = select_targets(_rows(), ("20s", "30s"), rebuild=True)

    assert [(item["content_key"], item["target_durations"]) for item in targets] == [
        ("002-partial", ["20s"]),
        ("003-all", ["20s", "30s"]),
    ]


def test_select_targets_honors_duration_and_content_key_filters() -> None:
    targets = select_targets(
        _rows(), ("30s",), rebuild=False, content_keys=["002-partial"]
    )

    assert len(targets) == 1
    assert targets[0]["content_key"] == "002-partial"
    assert targets[0]["target_durations"] == ["30s"]
