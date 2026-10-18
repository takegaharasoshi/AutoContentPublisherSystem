"""累積レビュー HTML、バッチ判定、manifest 台帳処理のテスト。"""

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
    load_item_lookup,
    load_seed_manifests,
    merge_manifests,
    paginate,
    sheet_page_name,
)


def _write_stock(root: Path, batch: str, items: list[dict]) -> None:
    batch_dir = root / batch
    batch_dir.mkdir(parents=True)
    (batch_dir / "stock_items.py").write_text(
        f"ITEMS = {items!r}\n", encoding="utf-8"
    )


def _item(content_key: str, title: str = "問題") -> dict:
    return {
        "content_key": content_key,
        "title": title,
        "hook": "フック",
        "problem_text": "問題文",
        "rule_text": "ルール",
        "character_lines": {
            "master": {"intro": "質問して", "outro": "コメントして"},
            "jr": {"outro": "フォローして"},
        },
        "play_example": [{"role": "questioner", "text": "質問"}],
        "caption": "キャプション",
        "truth": "真相",
        "fact_sheet": ["確定事実"],
    }


def test_review_html_escapes_content_and_resolves_media_from_review_dir(
    tmp_path: Path,
) -> None:
    manifest = {
        "001-test": {
            "video": "videos/<bad>.mp4",
            "bgm": {"track": "track01.m4a", "s3_key": "audio/&.m4a", "provisional": True},
            "narration": {
                "problem_sec": 10, "rule_sec": 5, "total_sec": 16.2,
                "tempo": 1.146, "engine_id": "gemini/gemini-3.8-flash-tts/voice-test",
            },
            "probe": {"width": 1080, "height": 1920, "fps": 30, "duration": 29, "audio_codec": "aac", "valid": True},
            "stills": {"intro": "stills/<intro>.jpg"},
        }
    }
    item = _item("001-test", '<危険>')
    item["hook"] = "A&B"
    item["problem_text"] = '<script>alert("x")</script>'

    html = generate_review_html(manifest, [item], base=tmp_path)

    assert "暫定 BGM が 1 件" in html
    assert "publish できません" in html
    assert "&lt;危険&gt;" in html
    assert "A&amp;B" in html
    assert "&lt;script&gt;" in html
    assert "<script>alert" not in html
    assert "../videos/&lt;bad&gt;.mp4" in html
    assert "../stills/&lt;intro&gt;.jpg" in html
    assert "×1.146" in html
    assert "gemini/gemini-3.8-flash-tts/voice-test" in html
    assert html.count('href="../review.html"') == 2


def test_review_html_shows_irodori_seed_without_tempo() -> None:
    manifest = {
        "001-test": {
            "narration": {
                "problem_sec": 8.0, "rule_sec": 8.0, "total_sec": 17.2,
                "engine_id": "irodori/model/kamerock-g4", "seed": 4, "seconds": 19.5,
            },
            "bgm": {}, "stills": {},
        },
    }
    html = generate_review_html(manifest, [_item("001-test")])

    assert "irodori/model/kamerock-g4 (seed=4, seconds=19.5)" in html
    assert "×" not in html


def test_unclassified_review_keeps_manifest_media_and_probe_without_item() -> None:
    manifest = {
        "099-removed": {
            "video": "videos/099-removed.mp4",
            "stills": {"intro": "stills/099-removed_intro.jpg"},
            "probe": {"width": 1080, "height": 1920, "fps": 30, "duration": 29, "valid": True},
        }
    }

    html = generate_review_html(manifest, {}, batch=UNCLASSIFIED)

    assert "素材なし" in html
    assert "../videos/099-removed.mp4" in html
    assert "../stills/099-removed_intro.jpg" in html
    assert "1080x1920 / 30fps / 29s" in html
    assert "stock_items.py に問題の素材がありません" in html


def test_sheet_page_name_and_pagination() -> None:
    assert sheet_page_name("batch-01", 1) == "batch-01.html"
    assert sheet_page_name("batch-01", 2) == "batch-01-2.html"
    manifest = {f"{stock_id:03}": {} for stock_id in range(1, 16)}

    pages = paginate(manifest, 14)

    assert [len(page) for page in pages] == [14, 1]
    assert list(pages[0]) == [f"{i:03}" for i in range(1, 15)]
    assert list(pages[1]) == ["015"]
    assert paginate({}, 14) == [{}]
    with pytest.raises(ValueError, match="1 以上"):
        paginate({"001": {}}, 0)


def test_merge_and_seed_manifests_preserve_order_and_validate_files(tmp_path: Path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    first.write_text(json.dumps({"001": {"value": "first"}, "002": {}}), encoding="utf-8")
    second.write_text(json.dumps({"001": {"value": "second"}}), encoding="utf-8")

    seeds = load_seed_manifests([first, second])
    merged = merge_manifests(
        {"001": {"value": "archive"}, "003": {}},
        seeds,
        {"001": {"value": "current"}},
    )

    assert merged == {"001": {"value": "current"}, "002": {}, "003": {}}
    with pytest.raises(RuntimeError, match="ありません"):
        load_seed_manifests([tmp_path / "missing.json"])
    broken = tmp_path / "broken.json"
    broken.write_text("{", encoding="utf-8")
    with pytest.raises(RuntimeError, match="読めません"):
        load_seed_manifests([broken])


def test_batch_detection_uses_content_key_and_keeps_unmatched_records(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    stock_root = tmp_path / "stock"
    _write_stock(stock_root, "batch-01", [_item("001-known", "既知")])
    (stock_root / "candidates").mkdir()
    bad = stock_root / "batch-broken"
    bad.mkdir()
    (bad / "stock_items.py").write_text("ITEMS = [", encoding="utf-8")

    lookup = load_item_lookup(stock_root)
    assigned = assign_batches(
        {
            "001-known": {"content_key": "001-known", "title": "台帳値"},
            "002-missing": {"content_key": "002-missing", "title": "外した素材"},
        },
        stock_root,
        item_lookup=lookup,
    )

    assert assigned["001-known"]["batch"] == "batch-01"
    assert assigned["002-missing"]["batch"] == UNCLASSIFIED
    assert lookup["001-known"][1]["title"] == "既知"
    assert "警告" in capsys.readouterr().err


def test_index_has_batch_links_current_marker_and_latest_video_mtime(tmp_path: Path) -> None:
    video = tmp_path / "work" / "videos" / "001.mp4"
    video.parent.mkdir(parents=True)
    video.write_bytes(b"video")
    timestamp = datetime(2026, 10, 17, 12, 34, tzinfo=timezone.utc).timestamp()
    os.utime(video, (timestamp, timestamp))
    newer_video = video.parent / "002.mp4"
    newer_video.write_bytes(b"video")
    os.utime(newer_video, (timestamp + 60, timestamp + 60))
    manifest = {
        "001": {"batch": "batch-02", "video": "videos/001.mp4"},
        "002": {"batch": "batch-02", "video": "videos/002.mp4"},
        "003": {"batch": "batch-01"},
        "004": {"batch": UNCLASSIFIED},
    }

    html = generate_index_html(
        manifest, current_batch="batch-02", per_page=1,
        base=tmp_path, work_dir=tmp_path / "work",
    )

    assert "全体: 4 件" in html
    assert html.index("batch-02") < html.index("batch-01")
    assert 'href="review/batch-02.html"' in html
    assert 'href="review/batch-02-2.html"' in html
    assert "今回" in html
    assert "2026-10-17 21:35 JST" in html
    assert "stock_items.py に無い問題（ビルド後に外した等）" in html


def test_main_seeds_archive_writes_batch_pages_and_removes_stale_outputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    base = tmp_path / "project"
    work = base / "work"
    work.mkdir(parents=True)
    monkeypatch.setattr(review_sheet, "BASE", base)
    monkeypatch.setattr(review_sheet, "WORK", work)
    stock_root = tmp_path / "stock"
    _write_stock(stock_root, "batch-01", [_item("001-old", "古い問題")])
    _write_stock(stock_root, "batch-02", [_item("002-current", "今回の問題")])
    seed = tmp_path / "seed.json"
    seed.write_text(
        json.dumps({"001-old": {"content_key": "001-old", "video": "videos/001-old.mp4"}}),
        encoding="utf-8",
    )
    (work / "manifest.json").write_text(
        json.dumps({
            "002-current": {"content_key": "002-current", "video": "videos/002-current.mp4"},
            "099-removed": {
                "content_key": "099-removed", "video": "videos/099-removed.mp4",
                "stills": {"intro": "stills/099-removed_intro.jpg"},
                "probe": {"width": 1080, "height": 1920, "fps": 30, "duration": 29, "valid": True},
            },
        }),
        encoding="utf-8",
    )
    (work / "review-2.html").write_text("stale", encoding="utf-8")
    stale_sheet = work / "review" / "stale.html"
    stale_sheet.parent.mkdir()
    stale_sheet.write_text("stale", encoding="utf-8")

    result = review_sheet.main([
        "--seed-from", str(seed), "--stock-root", str(stock_root), "--per-page", "1",
        "--batch", "batch-02",
    ])

    archive = json.loads((work / "review_archive.json").read_text(encoding="utf-8"))
    index = (work / "review.html").read_text(encoding="utf-8")
    old_sheet = (work / "review" / "batch-01.html").read_text(encoding="utf-8")
    current_sheet = (work / "review" / "batch-02.html").read_text(encoding="utf-8")
    orphan_sheet = (work / "review" / f"{UNCLASSIFIED}.html").read_text(encoding="utf-8")
    assert result == 0
    assert set(archive) == {"001-old", "002-current", "099-removed"}
    assert archive["001-old"]["batch"] == "batch-01"
    assert archive["002-current"]["batch"] == "batch-02"
    assert archive["099-removed"]["batch"] == UNCLASSIFIED
    assert 'href="review/batch-01.html"' in index
    assert 'href="review/batch-02.html"' in index
    assert "今回" in index
    assert "今回" in index[index.index("batch-02"):index.index("batch-01")]
    assert "古い問題" in old_sheet
    assert "今回の問題" in current_sheet
    assert "../videos/099-removed.mp4" in orphan_sheet
    assert not (work / "review-2.html").exists()
    assert not stale_sheet.exists()
    stdout = capsys.readouterr().out
    assert "インデックス:" in stdout
    assert "batch-01.html（1 件）" in stdout

def test_content_key_filter_limits_sheets_but_not_accumulated_archive(
    tmp_path: Path,
) -> None:
    base = tmp_path / "project"
    work = base / "work"
    work.mkdir(parents=True)
    (work / "manifest.json").write_text(
        json.dumps({"001": {"content_key": "001"}, "002": {"content_key": "002"}}),
        encoding="utf-8",
    )
    stock_root = tmp_path / "stock"
    _write_stock(stock_root, "batch-01", [_item("001"), _item("002")])
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(review_sheet, "BASE", base)
    monkeypatch.setattr(review_sheet, "WORK", work)
    try:
        review_sheet.write_review(
            content_keys=["002"], stock_root=stock_root, batch="batch-01"
        )
    finally:
        monkeypatch.undo()

    archive = json.loads((work / "review_archive.json").read_text(encoding="utf-8"))
    sheet = (work / "review" / "batch-01.html").read_text(encoding="utf-8")
    assert set(archive) == {"001", "002"}
    assert "002 — 問題" in sheet
    assert "001 — 問題" not in sheet
