"""Offline checks for the batch material review index."""

from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path

from tools import review_index


def _write_batch(root: Path, batch: str, count: int) -> Path:
    batch_dir = root / batch
    batch_dir.mkdir(parents=True)
    items = [{"content_key": "key-{}".format(index)} for index in range(count)]
    (batch_dir / "stock_items.py").write_text(
        "ITEMS = {!r}\n".format(items), encoding="utf-8"
    )
    return batch_dir


def test_index_lists_stock_counts_sheet_links_and_jst_mtime(tmp_path: Path) -> None:
    first = _write_batch(tmp_path, "batch-01", 2)
    second = _write_batch(tmp_path, "batch-02", 1)
    candidates = tmp_path / "candidates"
    candidates.mkdir()
    sheet = first / "work" / "review.html"
    sheet.parent.mkdir()
    sheet.write_text("review", encoding="utf-8")
    timestamp = datetime(2026, 10, 17, 12, 34, tzinfo=timezone.utc).timestamp()
    os.utime(sheet, (timestamp, timestamp))
    (second / "work").mkdir()

    html = review_index.generate_index_html(tmp_path)

    assert html.index("batch-01") < html.index("batch-02")
    assert "2 問" in html
    assert "1 問" in html
    assert 'href="../batch-01/work/review.html"' in html
    assert "未生成" in html
    assert "2026-10-17 21:34 JST" in html
    assert "candidates" not in html


def test_write_index_uses_requested_output_path(tmp_path: Path) -> None:
    root = tmp_path / "set"
    _write_batch(root, "batch-01", 0)
    output = tmp_path / "custom" / "index.html"

    result = review_index.write_index(root, output)

    assert result == output
    assert "batch-01" in output.read_text(encoding="utf-8")
