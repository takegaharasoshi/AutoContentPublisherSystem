"""素材レビューシートのバッチ別インデックスを生成する。"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
import runpy
import sys
from typing import List, Optional, Tuple
from urllib.parse import quote


SET_ROOT = Path(__file__).resolve().parents[1]
JST = timezone(timedelta(hours=9))


def _batch_rows(root: Path) -> List[Tuple[str, int, str, Optional[str]]]:
    """各 batch-* の素材数、更新日時、リンクを集める。"""
    rows: List[Tuple[str, int, str, Optional[str]]] = []
    if not root.is_dir():
        return rows
    for batch_dir in sorted(root.iterdir(), key=lambda path: path.name):
        if not batch_dir.is_dir() or not batch_dir.name.startswith("batch-"):
            continue
        stock_path = batch_dir / "stock_items.py"
        count = 0
        if stock_path.is_file():
            try:
                items = runpy.run_path(str(stock_path)).get("ITEMS")
                if not isinstance(items, list):
                    raise ValueError("ITEMS が list ではありません")
                count = len(items)
            except Exception as exc:
                print(f"警告: 素材数を取得できません: {stock_path}: {exc}", file=sys.stderr)

        sheet = batch_dir / "work" / "review.html"
        if sheet.is_file():
            updated = datetime.fromtimestamp(sheet.stat().st_mtime, timezone.utc)
            updated_label = updated.astimezone(JST).strftime("%Y-%m-%d %H:%M JST")
            href = "../{}/work/review.html".format(quote(batch_dir.name))
        else:
            updated_label = "—"
            href = None
        rows.append((batch_dir.name, count, updated_label, href))
    return rows


def generate_index_html(root: Path = SET_ROOT) -> str:
    """素材シートの一覧 HTML を返す。"""
    rows = []
    for batch, count, updated, href in _batch_rows(root):
        sheet_html = (
            '<a href="{}">素材シートを開く</a>'.format(escape(href, quote=True))
            if href is not None else "未生成"
        )
        rows.append(
            "<tr>"
            "<th>{}</th><td>{} 問</td><td>{}</td><td>{}</td>".format(
                escape(batch), count, escape(updated), sheet_html
            )
        )
    return """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>umigame-soup-1 素材レビューインデックス</title><style>
body{font-family:sans-serif;background:#f4f4f4;margin:24px;color:#222}
table{border-collapse:collapse;background:#fff;width:100%;margin-top:16px}
th,td{border:1px solid #ccc;padding:10px;text-align:left;vertical-align:top}
th{white-space:nowrap}a{color:#1b4e91}
@media(max-width:640px){body{margin:12px}th,td{padding:7px;font-size:13px}}
</style></head><body><h1>umigame-soup-1 素材レビューインデックス</h1>
<table><thead><tr><th>バッチ</th><th>問題数</th><th>素材シート更新日時</th>
<th>素材シート</th></tr></thead><tbody>""" + "\n".join(rows) + """
</tbody></table></body></html>
"""


def write_index(root: Path = SET_ROOT, output: Optional[Path] = None) -> Path:
    """セット直下の work/review.html にインデックスを書く。"""
    output_path = output or (root / "work" / "review.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generate_index_html(root), encoding="utf-8")
    return output_path


def main() -> int:
    """素材レビューインデックスを生成する。"""
    output = write_index()
    print("素材レビューインデックスを書き出しました: {}".format(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
