"""ビルド台帳から logic-training-1 の全数レビュー HTML を生成する。"""

from __future__ import annotations

import argparse
from html import escape
import os
from pathlib import Path
import re
import sys
from typing import Any

from common import BASE, WORK, load_json


SCRIPTS_DIR = BASE / "remotion" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from spec import STILL_FRAMES, STILL_LABELS  # noqa: E402


def _asset_path(value: Any, *, base: Path, fallback: Path) -> Path:
    """台帳のパスを優先し、無い場合は既定パスを返す。"""
    if isinstance(value, str) and value:
        path = Path(value)
        return path if path.is_absolute() else base / path
    return fallback


def _relative_asset(path: Path, work: Path) -> str:
    """review.html から参照できる POSIX 形式の相対 URL を返す。"""
    return Path(os.path.relpath(path, work)).as_posix()


def page_name(page: int) -> str:
    """ページ番号に対応するレビュー HTML のファイル名を返す。"""
    return "review.html" if page <= 1 else f"review-{page}.html"


def paginate(manifest: dict[str, Any], per_page: int) -> list[dict[str, Any]]:
    """台帳を stock_item_id 昇順で per_page 件ずつに分ける。

    スマホでは 1 ページに動画を並べすぎると後半のメディアが読み込まれないため、
    ページを分けて 1 ページあたりの読み込み量を抑える。
    """
    if per_page <= 0:
        raise ValueError("--per-page は 1 以上にしてください")
    stock_ids = sorted(manifest, key=int)
    return [
        {stock_id: manifest[stock_id] for stock_id in stock_ids[start:start + per_page]}
        for start in range(0, len(stock_ids), per_page)
    ] or [{}]


def _nav_html(page: int, total_pages: int, total_items: int) -> str:
    """ページ切り替えリンクを返す（1 ページのみなら空文字）。"""
    if total_pages <= 1:
        return ""
    links = []
    for number in range(1, total_pages + 1):
        label = f"{number} / {total_pages}"
        if number == page:
            links.append(f'<strong class="current">{label}</strong>')
        else:
            links.append(f'<a href="{page_name(number)}">{label}</a>')
    return (
        f'<nav class="pager"><span>ページ {page} / {total_pages}'
        f'（全 {total_items} 件）</span>{"".join(links)}</nav>'
    )


def generate_review_html(
    manifest: dict[str, Any],
    *,
    base: Path = BASE,
    page: int = 1,
    total_pages: int = 1,
    total_items: int | None = None,
) -> str:
    """ビルド台帳から、値をエスケープしたレビュー HTML を返す。"""
    work = base / "work"
    nav = _nav_html(
        page,
        total_pages,
        len(manifest) if total_items is None else total_items,
    )
    cards: list[str] = []
    for stock_id in sorted(manifest, key=int):
        record = manifest[stock_id]
        if not isinstance(record, dict):
            continue
        video = _asset_path(
            record.get("video"),
            base=base,
            fallback=work / "videos" / f"{stock_id}.mp4",
        )
        still_records = record.get("stills")
        still_records = still_records if isinstance(still_records, dict) else {}
        still_blocks: list[str] = []
        for key in STILL_FRAMES:
            value = still_records.get(key)
            fallback = work / "cuts" / f"{stock_id}_{key}.png"
            if not isinstance(value, str) or not value:
                if not fallback.is_file():
                    continue
                path = fallback
            else:
                path = _asset_path(value, base=base, fallback=fallback)
            source = escape(_relative_asset(path, work), quote=True)
            label = escape(STILL_LABELS[key])
            alt = escape(f"{stock_id} {STILL_LABELS[key]}", quote=True)
            still_blocks.append(
                f'<figure class="still still-{escape(key, quote=True)}">'
                f'<img src="{source}" alt="{alt}"><figcaption>{label}'
                "</figcaption></figure>"
            )

        illustration = work / "illustrations" / f"{stock_id}.png"
        stock_label = escape(str(stock_id))
        question = escape(str(record.get("question_text", "")))
        hint = escape(str(record.get("hint", "")))
        slot_code = escape(str(record.get("slot_code", "")))
        content_key = escape(str(record.get("content_key", "")))
        cards.append(
            f"<section><h2>stock_item_id: {stock_label}</h2>"
            '<div class="review-media"><div><h3>① 動画</h3>'
            '<video controls preload="metadata" '
            f'src="{escape(_relative_asset(video, work), quote=True)}"></video>'
            '</div><div class="still-area"><h3>② スチル</h3>'
            f'<div class="stills">{"".join(still_blocks)}</div></div></div>'
            '<h3>③ イラスト</h3><img class="illustration" '
            f'src="{escape(_relative_asset(illustration, work), quote=True)}" '
            f'alt="illustration {escape(stock_label, quote=True)}">'
            f'<div class="copy"><h3>④ 問題文と hint</h3>'
            f'<p class="question">{question}</p><p class="hint">hint: {hint}</p></div>'
            f'<p class="meta">⑤ slot_code: {slot_code} / '
            f"content_key: {content_key}</p></section>"
        )
    return """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<title>logic-training-1 動画レビュー</title><style>
body{font-family:sans-serif;background:#f4f4f4;margin:24px;color:#222}
section{background:#fff;padding:20px;margin:20px 0;border-radius:10px}
h2{font-size:18px;margin-top:0}h3{font-size:15px;margin:12px 0 6px}
.review-media{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}
video{width:270px;max-height:480px;background:#111}
.still-area{flex:1;min-width:360px}.stills{display:flex;gap:8px;flex-wrap:wrap}
.still{width:150px;margin:0;order:2}.still img{width:150px;display:block}
.still figcaption{font-size:12px;margin-top:4px}.still-seam_head{order:0}
.still-seam_tail{order:1}.illustration{width:360px;max-width:100%;display:block}
.question,.hint,.meta{font-size:14px}.hint{color:#555}.meta{margin-bottom:0}
.pager{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:#fff;
padding:12px 16px;border-radius:10px;font-size:14px;margin:16px 0}
.pager a,.pager .current{padding:6px 12px;border-radius:6px;text-decoration:none}
.pager a{background:#eef1f6;color:#1b2a4a}.pager .current{background:#1b2a4a;color:#fff}
</style></head><body><h1>logic-training-1 事前動画レビュー</h1>
<p>全数確認: 文字・数字・記号の混入、画風、情景適合、版面
（Instagram UI と重ならないか）、ループ継ぎ目
（先頭と末尾のスチルが一致しているか）、音。</p>
""" + nav + "\n".join(cards) + nav + "</body></html>\n"


def filter_manifest(
    manifest: dict[str, Any], slot_codes: list[str] | None
) -> dict[str, Any]:
    """指定スロットのエントリのみに絞る。

    昼（noon）のように凍結中で再ビルドしないスロットをレビュー対象から外す。
    """
    if not slot_codes:
        return dict(manifest)
    requested = set(slot_codes)
    return {
        stock_id: record
        for stock_id, record in manifest.items()
        if str(record.get("slot_code", "")) in requested
    }


def main(argv: list[str] | None = None) -> int:
    """work/build_manifest.json から work/review.html を書き出す。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--slot",
        action="append",
        metavar="SLOT_CODE",
        help="対象スロット（morning / noon / night。複数指定可）",
    )
    parser.add_argument(
        "--per-page",
        type=int,
        default=14,
        metavar="N",
        help="1 ページあたりの動画数（既定 14。スマホでの読み込み量を抑える）",
    )
    args = parser.parse_args(argv)
    manifest = load_json(WORK / "build_manifest.json", {})
    if not isinstance(manifest, dict):
        raise RuntimeError("work/build_manifest.json は JSON オブジェクトにしてください")
    manifest = filter_manifest(manifest, args.slot)
    pages = paginate(manifest, args.per_page)
    WORK.mkdir(parents=True, exist_ok=True)
    for stale in WORK.glob("review-*.html"):
        if re.fullmatch(r"review-\d+\.html", stale.name):
            stale.unlink()
    for index, page_manifest in enumerate(pages, start=1):
        output = WORK / page_name(index)
        output.write_text(
            generate_review_html(
                page_manifest,
                page=index,
                total_pages=len(pages),
                total_items=len(manifest),
            ),
            encoding="utf-8",
        )
        print(f"  {output.name}: {len(page_manifest)} 件")
    print(
        f"レビューシートを書き出しました: {WORK}"
        f"（全 {len(manifest)} 件 / {len(pages)} ページ・1 ページ {args.per_page} 件）"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
