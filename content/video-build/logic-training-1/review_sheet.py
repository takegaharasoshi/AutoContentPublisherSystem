"""累積ビルド台帳から logic-training-1 のレビューインデックスとシートを生成する。"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import runpy
import sys
from typing import Any, Iterable
from urllib.parse import quote

from common import BASE, ROOT, WORK, dump_json


SCRIPTS_DIR = BASE / "remotion" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from spec import STILL_FRAMES, STILL_LABELS  # noqa: E402


DEFAULT_STOCK_ROOT = ROOT / "content" / "quiz-stock" / "logic-training-1"
UNCLASSIFIED = "未分類"
UNCLASSIFIED_NOTE = '<br><small>stock_items.py に無い問題（完成稿 NG で差し戻した等）</small>'
JST = timezone(timedelta(hours=9))


def _asset_path(value: Any, *, base: Path, fallback: Path) -> Path:
    """台帳のパスを優先し、無い場合は既定パスを返す。"""
    if isinstance(value, str) and value:
        path = Path(value)
        return path if path.is_absolute() else base / path
    return fallback


def _relative_asset(path: Path, review_dir: Path) -> str:
    """レビューシートから参照できる POSIX 形式の相対 URL を返す。"""
    return Path(os.path.relpath(path, review_dir)).as_posix()


def sheet_page_name(batch: str, page: int) -> str:
    """バッチとページ番号に対応するシート名を返す。"""
    return f"{batch}.html" if page <= 1 else f"{batch}-{page}.html"


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


def _sheet_navigation(
    batch: str, page: int, total_pages: int, total_items: int
) -> str:
    """インデックスへの戻りリンクとページ切り替えを返す。"""
    pager = ""
    if total_pages > 1:
        links = []
        for number in range(1, total_pages + 1):
            label = f"{number} / {total_pages}"
            if number == page:
                links.append(f'<strong class="current">{label}</strong>')
            else:
                href = quote(sheet_page_name(batch, number))
                links.append(f'<a href="{href}">{label}</a>')
        pager = (
            f'<nav class="pager"><span>ページ {page} / {total_pages}'
            f'（全 {total_items} 件）</span>{"".join(links)}</nav>'
        )
    return (
        '<div class="sheet-navigation"><p><a href="../review.html">'
        '← インデックスへ戻る</a></p>'
        f"{pager}</div>"
    )


def generate_review_html(
    manifest: dict[str, Any],
    *,
    base: Path = BASE,
    batch: str = "",
    page: int = 1,
    total_pages: int = 1,
    total_items: int | None = None,
) -> str:
    """ビルド台帳から、値をエスケープしたバッチ別レビュー HTML を返す。"""
    work = base / "work"
    review_dir = work / "review"
    navigation = _sheet_navigation(
        batch,
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
            source = escape(_relative_asset(path, review_dir), quote=True)
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
            f'src="{escape(_relative_asset(video, review_dir), quote=True)}"></video>'
            '</div><div class="still-area"><h3>② スチル</h3>'
            f'<div class="stills">{"".join(still_blocks)}</div></div></div>'
            '<h3>③ イラスト</h3><img class="illustration" '
            f'src="{escape(_relative_asset(illustration, review_dir), quote=True)}" '
            f'alt="illustration {escape(stock_label, quote=True)}">'
            f'<div class="copy"><h3>④ 問題文と hint</h3>'
            f'<p class="question">{question}</p><p class="hint">hint: {hint}</p></div>'
            f'<p class="meta">⑤ slot_code: {slot_code} / '
            f"content_key: {content_key}</p></section>"
        )
    escaped_batch = escape(batch)
    return """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
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
.sheet-navigation>p{margin:12px 0}
/* スマホ縦持ち: 横スクロールを出さず、動画とイラストを画面幅いっぱいで見る */
@media (max-width:640px){
body{margin:12px}section{padding:14px;margin:14px 0}
.review-media{gap:12px}video{width:100%;max-height:none}
.still-area{min-width:0;width:100%}.still{width:calc(50% - 4px)}.still img{width:100%}
.illustration{width:100%}
.pager a,.pager .current{padding:12px 16px;min-height:44px;box-sizing:border-box}
}
</style></head><body><h1>logic-training-1 事前動画レビュー: """ + escaped_batch + """</h1>
<p>全数確認: 文字・数字・記号の混入、画風、情景適合、版面
（Instagram UI と重ならないか）、ループ継ぎ目
（先頭と末尾のスチルが一致しているか）、音。</p>
""" + navigation + "\n" + "\n".join(cards) + navigation + "</body></html>\n"


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
        if isinstance(record, dict)
        and str(record.get("slot_code", "")) in requested
    }


def _load_manifest(path: Path, *, required: bool) -> dict[str, Any]:
    """JSON manifest を読み、オブジェクトであることを確認する。"""
    if not path.is_file():
        if required:
            raise RuntimeError(f"manifest がありません: {path}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"manifest を読めません: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"manifest は JSON オブジェクトにしてください: {path}")
    return value


def load_seed_manifests(paths: Iterable[Path]) -> list[dict[str, Any]]:
    """指定順に必須の seed manifest を読み込む。"""
    return [_load_manifest(Path(path), required=True) for path in paths]


def merge_manifests(
    archive: dict[str, Any],
    seeds: Iterable[dict[str, Any]],
    current: dict[str, Any],
) -> dict[str, Any]:
    """既存台帳、seed の指定順、今回 manifest の順にマージする。"""
    merged = dict(archive)
    for manifest in seeds:
        merged.update(manifest)
    merged.update(current)
    return merged


def load_batch_lookup(stock_root: Path) -> dict[str, str]:
    """stock_items.py の question 文字列からバッチ名への対応を作る。"""
    lookup: dict[str, str] = {}
    if not stock_root.is_dir():
        return lookup
    for batch_dir in sorted(stock_root.iterdir(), key=lambda path: path.name):
        if not batch_dir.is_dir():
            continue
        stock_file = batch_dir / "stock_items.py"
        if not stock_file.is_file():
            continue
        try:
            items = runpy.run_path(str(stock_file)).get("ITEMS")
            if not isinstance(items, list):
                raise ValueError("ITEMS が list ではありません")
            for item in items:
                if not isinstance(item, dict):
                    continue
                question = item.get("question")
                if isinstance(question, str):
                    lookup[question] = batch_dir.name
        except Exception as exc:
            print(f"警告: バッチを読み込めません: {stock_file}: {exc}", file=sys.stderr)
    return lookup


def assign_batches(manifest: dict[str, Any], stock_root: Path) -> dict[str, Any]:
    """各レコードの batch を stock_items.py との一致から付け直す。"""
    lookup = load_batch_lookup(stock_root)
    assigned: dict[str, Any] = {}
    for key, value in manifest.items():
        if not isinstance(value, dict):
            assigned[key] = value
            continue
        record = dict(value)
        question = record.get("question_text")
        record["batch"] = lookup.get(question, UNCLASSIFIED)
        assigned[key] = record
    return assigned


def _record_video_paths(record: dict[str, Any], base: Path) -> list[Path]:
    """台帳レコードから動画パスを得る。"""
    value = record.get("video")
    if not isinstance(value, str) or not value:
        return []
    path = Path(value)
    return [path if path.is_absolute() else base / path]


def _last_build_label(records: dict[str, Any], base: Path) -> str:
    """バッチ内の動画ファイルで最新の mtime を JST 分単位で返す。"""
    timestamps = [
        path.stat().st_mtime
        for record in records.values()
        if isinstance(record, dict)
        for path in _record_video_paths(record, base)
        if path.is_file()
    ]
    if not timestamps:
        return "—"
    latest = datetime.fromtimestamp(max(timestamps), timezone.utc).astimezone(JST)
    return latest.strftime("%Y-%m-%d %H:%M JST")


def generate_index_html(
    manifest: dict[str, Any],
    current_manifest: dict[str, Any],
    *,
    per_page: int,
    base: Path = BASE,
) -> str:
    """バッチ別シートへのリンクを持つレビューインデックスを返す。"""
    groups: dict[str, dict[str, Any]] = {}
    current_batches: set[str] = set()
    for key, record in manifest.items():
        if not isinstance(record, dict):
            continue
        batch = str(record.get("batch") or UNCLASSIFIED)
        groups.setdefault(batch, {})[key] = record
    for record in current_manifest.values():
        if isinstance(record, dict):
            current_batches.add(str(record.get("batch") or UNCLASSIFIED))

    total_items = sum(len(records) for records in groups.values())
    rows: list[str] = []
    for batch in sorted(groups, reverse=True):
        records = groups[batch]
        morning = sum(record.get("slot_code") == "morning" for record in records.values())
        noon = sum(record.get("slot_code") == "noon" for record in records.values())
        night = sum(record.get("slot_code") == "night" for record in records.values())
        page_count = max(1, (len(records) + per_page - 1) // per_page)
        page_links = " ".join(
            f'<a href="review/{quote(sheet_page_name(batch, page))}">'
            f'{page}ページ目</a>'
            for page in range(1, page_count + 1)
        )
        marker = ' <strong class="current">今回</strong>' if batch in current_batches else ""
        count = (
            f"{len(records)} 件（朝 {morning} / 昼 {noon} / 夜 {night}）"
        )
        rows.append(
            "<tr>"
            f"<th>{escape(batch)}{marker}{UNCLASSIFIED_NOTE if batch == UNCLASSIFIED else ''}</th>"
            f"<td>{count}</td>"
            f"<td>{escape(_last_build_label(records, base))}</td>"
            f"<td>{page_links}</td></tr>"
        )
    return """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>logic-training-1 レビューインデックス</title><style>
body{font-family:sans-serif;background:#f4f4f4;margin:24px;color:#222}
table{border-collapse:collapse;background:#fff;width:100%;margin-top:16px}
th,td{border:1px solid #ccc;padding:10px;text-align:left;vertical-align:top}
th{white-space:nowrap}.current{color:#a33;margin-left:8px}
a{margin-right:10px}.summary{font-size:18px}
@media(max-width:640px){body{margin:12px}th,td{padding:7px;font-size:13px}}
</style></head><body><h1>logic-training-1 レビューインデックス</h1>
<p class="summary">全体: """ + str(total_items) + """ 件</p>
<table><thead><tr><th>バッチ</th><th>件数</th><th>最終ビルド日時</th>
<th>シート</th></tr></thead><tbody>""" + "\n".join(rows) + """
</tbody></table></body></html>
"""


def _cleanup_outputs(work: Path, review_dir: Path, expected: set[str]) -> None:
    """旧分割ファイルと今回生成しないバッチシートを削除する。"""
    for stale in work.glob("review-*.html"):
        if re.fullmatch(r"review-\d+\.html", stale.name):
            stale.unlink()
    for stale in review_dir.rglob("*.html"):
        if stale.relative_to(review_dir).as_posix() not in expected:
            stale.unlink()


def main(argv: list[str] | None = None) -> int:
    """累積台帳を更新し、インデックスとバッチ別シートを書き出す。"""
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
        help="1 シートあたりの動画数（既定 14）",
    )
    parser.add_argument(
        "--seed-from",
        nargs="+",
        type=Path,
        metavar="FILE",
        help="過去の manifest JSON を指定順に台帳へ追加する",
    )
    parser.add_argument(
        "--stock-root",
        type=Path,
        default=DEFAULT_STOCK_ROOT,
        help="バッチ判定に使う stock_items.py の親ディレクトリ",
    )
    args = parser.parse_args(argv)
    if args.per_page <= 0:
        parser.error("--per-page は 1 以上にしてください")

    current = _load_manifest(WORK / "build_manifest.json", required=False)
    archive_path = WORK / "review_archive.json"
    archive = _load_manifest(archive_path, required=False)
    seeds = load_seed_manifests(args.seed_from or [])
    merged = merge_manifests(archive, seeds, current)
    merged = assign_batches(merged, args.stock_root)
    dump_json(archive_path, merged)

    filtered = filter_manifest(merged, args.slot)
    current_tagged = {key: merged[key] for key in current if key in merged}
    filtered_current = filter_manifest(current_tagged, args.slot)
    groups: dict[str, dict[str, Any]] = {}
    for key, record in filtered.items():
        if isinstance(record, dict):
            groups.setdefault(str(record.get("batch") or UNCLASSIFIED), {})[key] = record

    review_dir = WORK / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    expected: set[str] = set()
    outputs: list[tuple[Path, int]] = []
    for batch in sorted(groups, reverse=True):
        batch_manifest = groups[batch]
        pages = paginate(batch_manifest, args.per_page)
        for page_number, page_manifest in enumerate(pages, start=1):
            filename = sheet_page_name(batch, page_number)
            expected.add(filename)
            output = review_dir / filename
            output.write_text(
                generate_review_html(
                    page_manifest,
                    base=BASE,
                    batch=batch,
                    page=page_number,
                    total_pages=len(pages),
                    total_items=len(batch_manifest),
                ),
                encoding="utf-8",
            )
            outputs.append((output, len(page_manifest)))

    index_path = WORK / "review.html"
    index_path.write_text(
        generate_index_html(
            filtered, filtered_current, per_page=args.per_page, base=BASE
        ),
        encoding="utf-8",
    )
    _cleanup_outputs(WORK, review_dir, expected)
    print(f"インデックス: {index_path}（全 {len(filtered)} 件）")
    for output, item_count in outputs:
        print(f"シート: {output}（{item_count} 件）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
