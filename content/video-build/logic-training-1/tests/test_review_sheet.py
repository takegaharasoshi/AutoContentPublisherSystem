"""累積レビュー HTML と manifest 処理のテスト。"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone

import pytest

import review_sheet
from review_sheet import (
    UNCLASSIFIED,
    assign_batches,
    filter_manifest,
    generate_index_html,
    generate_review_html,
    load_seed_manifests,
    merge_manifests,
    paginate,
    sheet_page_name,
)
from spec import STILL_FRAMES


def _write_stock(root: Path, batch: str, questions: list[str]) -> None:
    batch_dir = root / batch
    batch_dir.mkdir(parents=True)
    items = [{"question": question} for question in questions]
    (batch_dir / "stock_items.py").write_text(
        f"ITEMS = {items!r}\n", encoding="utf-8"
    )


def test_review_html_escapes_and_uses_media_paths_from_review_dir(tmp_path: Path) -> None:
    manifest = {
        "85": {
            "video": "work/videos/85.mp4",
            "stills": {
                key: f"work/cuts/85_{key}.png" for key in STILL_FRAMES
            },
            "question_text": '<script>alert("x")</script>',
            "hint": "A&B <ヒント>",
            "slot_code": "morning",
            "content_key": "logic<&>",
        }
    }

    html = generate_review_html(manifest, base=tmp_path, batch="2026-10-w1")

    assert "../videos/85.mp4" in html
    assert "../cuts/85_cut2.png" in html
    assert "../illustrations/85.png" in html
    assert "hint: A&amp;B &lt;ヒント&gt;" in html
    assert "logic&lt;&amp;&gt;" in html
    assert "<script>alert" not in html
    assert "&lt;script&gt;alert(&quot;" in html
    assert html.count('href="../review.html"') == 2


def test_review_html_keeps_stills_in_spec_order() -> None:
    manifest = {
        "1": {"stills": {key: f"work/cuts/1_{key}.png" for key in STILL_FRAMES}}
    }

    html = generate_review_html(manifest, batch="batch")
    positions = [html.index(f"1_{key}.png") for key in STILL_FRAMES]

    assert positions == sorted(positions)
    assert ".still-seam_head{order:0}" in html
    assert ".still-seam_tail{order:1}" in html


def test_filter_manifest_keeps_requested_slots_only() -> None:
    manifest = {
        "1": {"slot_code": "morning"},
        "2": {"slot_code": "noon"},
        "3": {"slot_code": "night"},
        "4": {},
    }

    assert filter_manifest(manifest, None) == manifest
    assert filter_manifest(manifest, []) == manifest
    assert sorted(filter_manifest(manifest, ["morning", "night"])) == ["1", "3"]


def test_sheet_page_name_and_pagination() -> None:
    assert sheet_page_name("2026-10-w1", 1) == "2026-10-w1.html"
    assert sheet_page_name("2026-10-w1", 2) == "2026-10-w1-2.html"
    manifest = {str(stock_id): {"slot_code": "morning"} for stock_id in range(1, 16)}

    pages = paginate(manifest, 14)

    assert [len(page) for page in pages] == [14, 1]
    assert list(pages[0]) == [str(i) for i in range(1, 15)]
    assert list(pages[1]) == ["15"]
    assert paginate({}, 14) == [{}]
    with pytest.raises(ValueError, match="1 以上"):
        paginate({"1": {}}, 0)


def test_merge_and_seed_manifests_preserve_order_and_validate_files(tmp_path: Path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    first.write_text(json.dumps({"1": {"value": "first"}, "2": {}}), encoding="utf-8")
    second.write_text(json.dumps({"1": {"value": "second"}}), encoding="utf-8")

    seeds = load_seed_manifests([first, second])
    merged = merge_manifests(
        {"1": {"value": "archive"}, "3": {}},
        seeds,
        {"1": {"value": "current"}},
    )

    assert merged == {
        "1": {"value": "current"},
        "2": {},
        "3": {},
    }
    with pytest.raises(RuntimeError, match="ありません"):
        load_seed_manifests([tmp_path / "missing.json"])
    broken = tmp_path / "broken.json"
    broken.write_text("{", encoding="utf-8")
    with pytest.raises(RuntimeError, match="読めません"):
        load_seed_manifests([broken])


def test_batch_detection_reassigns_batch_and_keeps_unmatched_records(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    stock_root = tmp_path / "stock"
    _write_stock(stock_root, "2026-10-w1", ["Exact question"])
    (stock_root / "candidates").mkdir()
    bad = stock_root / "broken"
    bad.mkdir()
    (bad / "stock_items.py").write_text("ITEMS = [", encoding="utf-8")

    assigned = assign_batches(
        {
            "1": {"question_text": "Exact question", "batch": "stale"},
            "2": {"question_text": " exact question "},
        },
        stock_root,
    )

    assert assigned["1"]["batch"] == "2026-10-w1"
    assert assigned["2"]["batch"] == UNCLASSIFIED
    assert "警告" in capsys.readouterr().err


def test_index_has_sorted_batch_links_current_marker_counts_and_latest_mtime(
    tmp_path: Path,
) -> None:
    video = tmp_path / "work" / "videos" / "1.mp4"
    video.parent.mkdir(parents=True)
    video.write_bytes(b"video")
    timestamp = datetime(2026, 10, 17, 12, 34, tzinfo=timezone.utc).timestamp()
    os.utime(video, (timestamp, timestamp))
    newer_video = video.parent / "2.mp4"
    newer_video.write_bytes(b"video")
    os.utime(newer_video, (timestamp + 60, timestamp + 60))
    manifest = {
        "1": {
            "batch": "2026-10-w1",
            "slot_code": "morning",
            "video": "work/videos/1.mp4",
        },
        "2": {
            "batch": "2026-10-w1",
            "slot_code": "night",
            "video": "work/videos/2.mp4",
        },
        "3": {"batch": "2026-09-w4", "slot_code": "night"},
    }

    html = generate_index_html(
        manifest, {"1": manifest["1"]}, per_page=1, base=tmp_path
    )

    assert "全体: 3 件" in html
    assert html.index("2026-10-w1") < html.index("2026-09-w4")
    assert 'href="review/2026-10-w1.html"' in html
    assert 'href="review/2026-10-w1-2.html"' in html
    assert "朝 1 / 昼 0 / 夜 1" in html
    assert "今回" in html
    assert "2026-10-17 21:35 JST" in html


def test_main_seeds_archive_writes_pages_and_removes_stale_outputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    base = tmp_path / "project"
    work = base / "work"
    work.mkdir(parents=True)
    monkeypatch.setattr(review_sheet, "BASE", base)
    monkeypatch.setattr(review_sheet, "WORK", work)
    stock_root = tmp_path / "stock"
    _write_stock(stock_root, "2026-10-w1", ["Old", "Current"])
    seed = tmp_path / "seed.json"
    seed.write_text(json.dumps({"1": {"question_text": "Old"}}), encoding="utf-8")
    (work / "build_manifest.json").write_text(
        json.dumps({"2": {"question_text": "Current", "slot_code": "morning"}}),
        encoding="utf-8",
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
    first_page = (work / "review" / "2026-10-w1.html").read_text(encoding="utf-8")
    second_page = (work / "review" / "2026-10-w1-2.html").read_text(encoding="utf-8")
    assert result == 0
    assert set(archive) == {"1", "2"}
    assert all(record["batch"] == "2026-10-w1" for record in archive.values())
    assert 'href="review/2026-10-w1.html"' in index
    assert 'href="review/2026-10-w1-2.html"' in index
    assert "今回" in index
    assert 'href="2026-10-w1-2.html"' in first_page
    assert 'href="2026-10-w1.html"' in second_page
    assert not (work / "review-2.html").exists()
    assert not stale_sheet.exists()
    stdout = capsys.readouterr().out
    assert "インデックス:" in stdout
    assert "2026-10-w1.html（1 件）" in stdout
