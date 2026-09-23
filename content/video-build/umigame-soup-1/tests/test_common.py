"""ストック読込・選択・manifest・S3 キーのテスト。"""

from __future__ import annotations

from pathlib import Path

import pytest

from common import (
    background_s3_key,
    load_items,
    load_manifest,
    save_manifest,
    select_items,
    video_s3_key,
)


def test_load_and_select_items() -> None:
    items = load_items("batch-01")

    assert len(items) == 14
    assert [item["content_key"] for item in select_items(
        items, ["001-faint-shadow", "014-kind-interpreter"]
    )] == ["001-faint-shadow", "014-kind-interpreter"]
    with pytest.raises(ValueError, match="未知の content_key"):
        select_items(items, ["999-missing"])


def test_s3_keys() -> None:
    assert video_s3_key("001-one") == "assets/umigame-soup-1/prebuilt/001-one.mp4"
    assert background_s3_key("001-one") == "assets/umigame-soup-1/prebuilt/001-one_bg.png"


def test_manifest_round_trip_and_default(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    assert load_manifest(path) == {}

    save_manifest({"001": {"title": "海亀"}}, path)

    assert load_manifest(path) == {"001": {"title": "海亀"}}
    assert not list(tmp_path.glob("*.tmp"))
