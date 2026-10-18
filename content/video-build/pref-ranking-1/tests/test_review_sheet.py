"""累積レビュー HTML と manifest 処理のテスト。"""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path

import pytest

import review_sheet
from review_sheet import (
    UNCLASSIFIED,
    assign_batches,
    generate_index_html,
    generate_review_html,
    load_seed_manifests,
    merge_manifests,
    paginate,
    sheet_page_name,
)


def _props(source: str = "資料", cue_text: str = "ナレーション") -> dict[str, object]:
    return {
        "subtitle": "全国平均",
        "sourceDisplay": source,
        "valuePrefix": "年間",
        "valueSuffix": "円",
        "entries": [{"rank": 1, "prefName": "宮崎県", "value": 1234}],
        "cues": {"intro": {"text": cue_text}},
    }


def _record(base: Path, content_key: str, title: str) -> dict[str, object]:
    durations: dict[str, object] = {}
    for duration in ("20s", "30s"):
        props_path = base / "work" / "props" / f"{content_key}-{duration}.json"
        props_path.parent.mkdir(parents=True, exist_ok=True)
        props_path.write_text(json.dumps(_props()), encoding="utf-8")
        durations[duration] = {
            "video": f"work/videos/{content_key}_{duration}.mp4",
            "props": f"work/props/{content_key}-{duration}.json",
            "loudness_i": -15.0,
            "loudness_tp": -1.1,
        }
    return {
        "content_key": content_key,
        "title": title,
        "audio_asset_id": 3,
        "bgm_s3_key": "audio/track.m4a",
        "durations": durations,
    }


def _write_stock(root: Path, batch: str, numbers: list[str]) -> None:
    batch_dir = root / batch
    batch_dir.mkdir(parents=True)
    items = [{"no": number} for number in numbers]
    (batch_dir / "stock_items.py").write_text(
        f"ITEMS = {items!r}\n", encoding="utf-8"
    )


def test_review_html_escapes_values_and_resolves_media_from_review_dir(
    tmp_path: Path,
) -> None:
    props_dir = tmp_path / "work" / "props"
    props_dir.mkdir(parents=True)
    for duration in ("20s", "30s"):
        (props_dir / f"001-{duration}.json").write_text(
            json.dumps(_props("A&B <出典>", '<script>alert("x")</script>')),
            encoding="utf-8",
        )
    manifest = {
        "001-unsafe": {
            "title": "<危険&タイトル>",
            "audio_asset_id": 3,
            "bgm_s3_key": "audio/&music.m4a",
            "durations": {
                "20s": {
                    "video": "work/videos/001_20s.mp4",
                    "props": "work/props/001-20s.json",
                    "loudness_i": -15.0,
                    "loudness_tp": -1.1,
                },
                "30s": {
                    "video": "work/videos/001_30s.mp4",
                    "props": "work/props/001-30s.json",
                    "loudness_i": -14.9,
                    "loudness_tp": -1.2,
                },
            },
        }
    }

    html = generate_review_html(manifest, base=tmp_path, batch="2026-08-initial")

    assert "../videos/001_20s.mp4" in html
    assert "../videos/001_30s.mp4" in html
    assert "../backgrounds/001-unsafe.png" in html
    assert "&lt;危険&amp;タイトル&gt;" in html
    assert "A&amp;B &lt;出典&gt;" in html
    assert "&lt;script&gt;alert(&quot;" in html
    assert "<script>alert" not in html
    assert html.count('href="../review.html"') == 2


def test_merge_seed_order_and_seed_file_errors(tmp_path: Path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    first.write_text(json.dumps({"001-a": {"title": "first"}, "003-c": {}}), encoding="utf-8")
    second.write_text(json.dumps({"001-a": {"title": "second"}}), encoding="utf-8")

    merged = merge_manifests(
        {"001-a": {"title": "archive"}, "004-d": {}},
        load_seed_manifests([first, second]),
        {"001-a": {"title": "current"}},
    )

    assert merged == {
        "001-a": {"title": "current"},
        "003-c": {},
        "004-d": {},
    }
    with pytest.raises(RuntimeError, match="ありません"):
        load_seed_manifests([tmp_path / "missing.json"])
    broken = tmp_path / "broken.json"
    broken.write_text("{", encoding="utf-8")
    with pytest.raises(RuntimeError, match="読めません"):
        load_seed_manifests([broken])


def test_batch_detection_and_unclassified_records(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    stock_root = tmp_path / "stock"
    _write_stock(stock_root, "2026-08-initial", ["001"])
    (stock_root / "candidates").mkdir()
    broken = stock_root / "broken"
    broken.mkdir()
    (broken / "stock_items.py").write_text("ITEMS = [", encoding="utf-8")

    assigned = assign_batches(
        {
            "001-known": {"content_key": "001-known", "batch": "stale"},
            "999-unknown": {"content_key": "999-unknown"},
        },
        stock_root,
    )

    assert assigned["001-known"]["batch"] == "2026-08-initial"
    assert assigned["999-unknown"]["batch"] == UNCLASSIFIED
    assert "警告" in capsys.readouterr().err


def test_index_has_pages_current_marker_and_latest_video_mtime(tmp_path: Path) -> None:
    video = tmp_path / "work" / "videos" / "001-20s.mp4"
    video.parent.mkdir(parents=True)
    video.write_bytes(b"video")
    timestamp = datetime(2026, 10, 17, 12, 34, tzinfo=timezone.utc).timestamp()
    os.utime(video, (timestamp, timestamp))
    newer_video = video.parent / "002-30s.mp4"
    newer_video.write_bytes(b"video")
    os.utime(newer_video, (timestamp + 120, timestamp + 120))
    manifest = {
        "001-a": {
            "batch": "2026-08-initial",
            "durations": {"20s": {"video": "work/videos/001-20s.mp4"}},
        },
        "002-b": {
            "batch": "2026-08-initial",
            "durations": {"30s": {"video": "work/videos/002-30s.mp4"}},
        },
        "003-c": {"batch": "2026-07-initial", "durations": {}},
    }

    html = generate_index_html(
        manifest,
        {"001-a": manifest["001-a"]},
        per_page=1,
        base=tmp_path,
    )

    assert "全体: 3 件" in html
    assert html.index("2026-08-initial") < html.index("2026-07-initial")
    assert 'href="review/2026-08-initial.html"' in html
    assert 'href="review/2026-08-initial-2.html"' in html
    assert 'href="review/2026-07-initial.html"' in html
    assert "今回" in html
    assert "2026-10-17 21:36 JST" in html


def test_pagination_and_sheet_page_names() -> None:
    manifest = {f"{number:03d}-item": {} for number in range(1, 16)}

    pages = paginate(manifest, 14)

    assert sheet_page_name("batch", 1) == "batch.html"
    assert sheet_page_name("batch", 2) == "batch-2.html"
    assert [len(page) for page in pages] == [14, 1]
    assert paginate({}, 14) == [{}]
    with pytest.raises(ValueError, match="1 以上"):
        paginate(manifest, 0)


def test_main_seeds_archive_splits_sheets_and_cleans_old_html(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    base = tmp_path / "project"
    work = base / "work"
    work.mkdir(parents=True)
    monkeypatch.setattr(review_sheet, "BASE", base)
    monkeypatch.setattr(review_sheet, "WORK", work)
    stock_root = tmp_path / "stock"
    _write_stock(stock_root, "2026-08-initial", ["001", "002"])
    seed = tmp_path / "seed.json"
    seed.write_text(
        json.dumps({"001-first": _record(base, "001-first", "First")}),
        encoding="utf-8",
    )
    current_record = _record(base, "002-second", "Second")
    (work / "build_manifest.json").write_text(
        json.dumps({"002-second": current_record}), encoding="utf-8"
    )
    (work / "review-2.html").write_text("stale", encoding="utf-8")
    stale_sheet = work / "review" / "stale.html"
    stale_sheet.parent.mkdir()
    stale_sheet.write_text("stale", encoding="utf-8")

    result = review_sheet.main(
        ["--seed-from", str(seed), "--stock-root", str(stock_root), "--per-page", "1"]
    )

    archive = json.loads((work / "review_archive.json").read_text(encoding="utf-8"))
    index = (work / "review.html").read_text(encoding="utf-8")
    first = (work / "review" / "2026-08-initial.html").read_text(encoding="utf-8")
    second = (work / "review" / "2026-08-initial-2.html").read_text(encoding="utf-8")
    assert result == 0
    assert set(archive) == {"001-first", "002-second"}
    assert all(record["batch"] == "2026-08-initial" for record in archive.values())
    assert 'href="review/2026-08-initial.html"' in index
    assert 'href="review/2026-08-initial-2.html"' in index
    assert "今回" in index
    assert '../videos/001-first_20s.mp4' in first
    assert 'href="2026-08-initial-2.html"' in first
    assert 'href="2026-08-initial.html"' in second
    assert not (work / "review-2.html").exists()
    assert not stale_sheet.exists()
    stdout = capsys.readouterr().out
    assert "インデックス:" in stdout
    assert "2026-08-initial.html（1 件）" in stdout
