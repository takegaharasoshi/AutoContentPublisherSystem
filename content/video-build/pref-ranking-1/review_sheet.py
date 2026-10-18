"""累積ビルド台帳から pref-ranking-1 のレビューインデックスとシートを生成する。"""

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

from common import BASE, ROOT, DURATIONS, WORK, dump_json, load_json


DEFAULT_STOCK_ROOT = ROOT / "content" / "ranking-stock" / "pref-ranking-1"
UNCLASSIFIED = "未分類"
UNCLASSIFIED_NOTE = '<br><small>stock_items.py に無いネタ</small>'
JST = timezone(timedelta(hours=9))


def _relative_asset(path: Path, review_dir: Path) -> str:
    """レビューシートから参照できる POSIX 形式の相対パスを返す。"""
    return Path(os.path.relpath(path, review_dir)).as_posix()


def _display_value(value: Any, props: dict[str, Any]) -> str:
    """順位行に出るのと同じ整形（前置き + 桁区切り + 単位）を返す。"""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return ""
    number = f"{value:,}" if float(value).is_integer() else f"{value:,.2f}"
    prefix = props.get("valuePrefix") or ""
    suffix = props.get("valueSuffix") or ""
    return f"{prefix}{number}{suffix}"


def _props_path(detail: dict[str, Any], base: Path) -> Path:
    value = detail.get("props")
    if not isinstance(value, str):
        raise RuntimeError("manifest の props パスがありません")
    path = Path(value)
    return path if path.is_absolute() else base / path


def sheet_page_name(batch: str, page: int) -> str:
    """バッチとページ番号に対応するシート名を返す。"""
    return f"{batch}.html" if page <= 1 else f"{batch}-{page}.html"


def paginate(manifest: dict[str, Any], per_page: int) -> list[dict[str, Any]]:
    """台帳を content_key 順で per_page 件ずつに分ける。"""
    if per_page <= 0:
        raise ValueError("--per-page は 1 以上にしてください")
    keys = sorted(manifest)
    return [
        {key: manifest[key] for key in keys[start:start + per_page]}
        for start in range(0, len(keys), per_page)
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
    """manifest と尺別 props からバッチ別のレビュー HTML を生成する。"""
    work = base / "work"
    review_dir = work / "review"
    navigation = _sheet_navigation(
        batch,
        page,
        total_pages,
        len(manifest) if total_items is None else total_items,
    )
    cards: list[str] = []
    for content_key in sorted(manifest):
        record = manifest[content_key]
        if not isinstance(record, dict):
            continue
        durations = record.get("durations", {})
        if not isinstance(durations, dict):
            continue
        duration_blocks: list[str] = []
        representative: dict[str, Any] | None = None
        for duration in DURATIONS:
            detail = durations.get(duration)
            if not isinstance(detail, dict):
                continue
            props_path = _props_path(detail, base)
            if not props_path.is_file():
                raise RuntimeError(
                    f"{content_key} {duration}: props がありません: {props_path}"
                )
            props = load_json(props_path, {})
            if not isinstance(props, dict):
                raise RuntimeError(f"{content_key} {duration}: props が不正です")
            representative = representative or props
            video_value = detail.get("video", "")
            video_path = (
                Path(video_value) if isinstance(video_value, str) else Path("")
            )
            if not video_path.is_absolute():
                video_path = base / video_path
            cues = props.get("cues", {})
            cue_items = ""
            if isinstance(cues, dict):
                cue_items = "".join(
                    f"<li><code>{escape(str(cue_id))}</code> "
                    f"{escape(str(cue.get('text', '')))}</li>"
                    for cue_id, cue in cues.items()
                    if isinstance(cue, dict)
                )
            loudness_i = escape(str(detail.get("loudness_i", "")))
            loudness_tp = escape(str(detail.get("loudness_tp", "")))
            duration_blocks.append(
                f'<div class="duration"><h3>{escape(duration)}</h3>'
                '<video controls preload="metadata" '
                f'src="{escape(_relative_asset(video_path, review_dir), quote=True)}">'
                "</video>"
                f"<p>実測: I={loudness_i} LUFS / TP={loudness_tp} dBFS</p>"
                f'<ol class="cues">{cue_items}</ol></div>'
            )
        if representative is None:
            continue
        fields = (
            ("subtitle", representative.get("subtitle")),
            ("source_display", representative.get("sourceDisplay")),
            ("value_prefix", representative.get("valuePrefix")),
            ("value_suffix", representative.get("valueSuffix")),
        )
        field_rows = "".join(
            f"<tr><th>{escape(label)}</th><td>"
            f"{escape(str(value if value is not None else ''))}</td></tr>"
            for label, value in fields
        )
        entries = "".join(
            "<tr>"
            f"<td>{escape(str(entry.get('rank', '')))}位</td>"
            f"<td>{escape(str(entry.get('prefName', '')))}</td>"
            f"<td>{escape(str(entry.get('value', '')))}</td>"
            f"<td>{escape(_display_value(entry.get('value'), representative))}</td>"
            "</tr>"
            for entry in representative.get("entries", [])
            if isinstance(entry, dict)
        )
        background = work / "backgrounds" / f"{content_key}.png"
        cards.append(
            f"<section><h2>{escape(content_key)} — "
            f"{escape(str(record.get('title', '')))}</h2>"
            f'<div class="media">{"".join(duration_blocks)}'
            '<div><h3>背景</h3><img class="background" '
            f'src="{escape(_relative_asset(background, review_dir), quote=True)}" '
            f'alt="背景 {escape(content_key, quote=True)}"></div></div>'
            f"<table>{field_rows}</table><h3>TOP5</h3>"
            "<table><tr><th>順位</th><th>都道府県</th><th>値</th>"
            f"<th>版面表示</th></tr>{entries}</table>"
            f"<p>BGM: audio_asset_id={escape(str(record.get('audio_asset_id', '')))} / "
            f"s3_key={escape(str(record.get('bgm_s3_key', '')))}</p></section>"
        )
    escaped_batch = escape(batch)
    return """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>pref-ranking-1 動画レビュー</title><style>
body{font-family:sans-serif;background:#f3f1eb;margin:24px;color:#222}
section{background:#fff;padding:20px;margin:20px 0;border-radius:10px}
.media{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}
.duration{width:300px}video{width:270px;max-height:480px;background:#111}
.background{width:270px;max-height:480px;object-fit:cover}
table{border-collapse:collapse;margin:12px 0}
th,td{border:1px solid #ccc;padding:6px 10px;text-align:left}
.cues{padding-left:24px;font-size:14px}code{font-weight:bold}
.pager{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:#fff;
padding:12px 16px;border-radius:10px;font-size:14px;margin:16px 0}
.pager a,.pager .current{padding:6px 12px;border-radius:6px;text-decoration:none}
.pager a{background:#eef1f6;color:#1b2a4a}.pager .current{background:#1b2a4a;color:#fff}
.sheet-navigation>p{margin:12px 0}
@media(max-width:640px){body{margin:12px}section{padding:14px;margin:14px 0}
.duration{width:100%}video,.background{width:100%;max-height:none}
.pager a,.pager .current{padding:12px 16px;min-height:44px;box-sizing:border-box}}
</style></head><body><h1>pref-ranking-1 事前動画レビュー: """ + escaped_batch + """</h1>
<p>全数・両尺を確認する。①背景イラストの品質（文字・数字・記号の混入、
和モダン調、版面の可読性） ②版面（県名・数値・金の可読性、見切れ、
地図と順位の整合） ③音（ナレーション同期、語尾切れ、BGM とのバランス）。</p>
""" + navigation + "\n" + "\n".join(cards) + navigation + "</body></html>\n"


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
    """stock_items.py の 3 桁 no からバッチ名への対応を作る。"""
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
                item_no = item.get("no")
                if isinstance(item_no, str) and re.fullmatch(r"\d{3}", item_no):
                    lookup[item_no] = batch_dir.name
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
        content_key = record.get("content_key", key)
        prefix = content_key[:3] if isinstance(content_key, str) else ""
        record["batch"] = lookup.get(prefix, UNCLASSIFIED)
        assigned[key] = record
    return assigned


def _record_video_paths(record: dict[str, Any], base: Path) -> list[Path]:
    """台帳レコードから尺別動画パスを得る。"""
    durations = record.get("durations", {})
    if not isinstance(durations, dict):
        return []
    paths: list[Path] = []
    for detail in durations.values():
        if not isinstance(detail, dict):
            continue
        value = detail.get("video")
        if not isinstance(value, str) or not value:
            continue
        path = Path(value)
        paths.append(path if path.is_absolute() else base / path)
    return paths


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
        page_count = max(1, (len(records) + per_page - 1) // per_page)
        page_links = " ".join(
            f'<a href="review/{quote(sheet_page_name(batch, page))}">'
            f'{page}ページ目</a>'
            for page in range(1, page_count + 1)
        )
        marker = ' <strong class="current">今回</strong>' if batch in current_batches else ""
        rows.append(
            "<tr>"
            f"<th>{escape(batch)}{marker}{UNCLASSIFIED_NOTE if batch == UNCLASSIFIED else ''}</th>"
            f"<td>{len(records)} 件</td>"
            f"<td>{escape(_last_build_label(records, base))}</td>"
            f"<td>{page_links}</td></tr>"
        )
    return """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>pref-ranking-1 レビューインデックス</title><style>
body{font-family:sans-serif;background:#f3f1eb;margin:24px;color:#222}
table{border-collapse:collapse;background:#fff;width:100%;margin-top:16px}
th,td{border:1px solid #ccc;padding:10px;text-align:left;vertical-align:top}
th{white-space:nowrap}.current{color:#a33;margin-left:8px}
a{margin-right:10px}.summary{font-size:18px}
@media(max-width:640px){body{margin:12px}th,td{padding:7px;font-size:13px}}
</style></head><body><h1>pref-ranking-1 レビューインデックス</h1>
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

    review_dir = WORK / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    expected: set[str] = set()
    outputs: list[tuple[Path, int]] = []
    groups: dict[str, dict[str, Any]] = {}
    for key, record in merged.items():
        if isinstance(record, dict):
            groups.setdefault(str(record.get("batch") or UNCLASSIFIED), {})[key] = record

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
            merged,
            {key: merged[key] for key in current if key in merged},
            per_page=args.per_page,
            base=BASE,
        ),
        encoding="utf-8",
    )
    _cleanup_outputs(WORK, review_dir, expected)
    print(f"インデックス: {index_path}（全 {len(merged)} 件）")
    for output, item_count in outputs:
        print(f"シート: {output}（{item_count} 件）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
