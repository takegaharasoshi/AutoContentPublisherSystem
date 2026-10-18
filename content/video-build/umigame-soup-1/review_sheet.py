"""累積ビルド台帳から umigame-soup-1 のレビューインデックスとシートを生成する。"""

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
from typing import Any, Iterable, Mapping
from urllib.parse import quote

from common import DURATION_SECONDS, ROOT, WORK, load_items


BASE = Path(__file__).resolve().parent
DEFAULT_STOCK_ROOT = ROOT / "content" / "umigame-stock" / "umigame-soup-1"
UNCLASSIFIED = "未分類"
UNCLASSIFIED_NOTE = (
    "<br><small>stock_items.py に無い問題（ビルド後に外した等）</small>"
)
JST = timezone(timedelta(hours=9))


def _text(value: object) -> str:
    """値を HTML テキストとしてエスケープする。"""
    return escape(str(value if value is not None else ""))


def _asset(value: object) -> str:
    """値を HTML 属性としてエスケープする。"""
    return escape(str(value if value is not None else ""), quote=True)


def _mapping(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _work_asset_path(value: object, *, base: Path, work_dir: Path) -> Path | None:
    """manifest の work 相対パスまたはプロジェクト相対パスを解決する。"""
    if not isinstance(value, str) or not value:
        return None
    if value.startswith(("http://", "https://")):
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == "work":
        return base / path
    return work_dir / path


def _relative_asset(value: object, *, base: Path, work_dir: Path, review_dir: Path) -> str:
    """シートから参照できるメディア URL を返す。"""
    if not isinstance(value, str) or not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    path = _work_asset_path(value, base=base, work_dir=work_dir)
    if path is None:
        return value
    return Path(os.path.relpath(path, review_dir)).as_posix()


def sheet_page_name(batch: str, page: int) -> str:
    """バッチとページ番号に対応するシート名を返す。"""
    return f"{batch}.html" if page <= 1 else f"{batch}-{page}.html"


def paginate(manifest: dict[str, Any], per_page: int) -> list[dict[str, Any]]:
    """content_key 順に per_page 件ずつ分ける。"""
    if per_page <= 0:
        raise ValueError("--per-page は 1 以上にしてください")
    keys = sorted(manifest)
    return [
        {key: manifest[key] for key in keys[start:start + per_page]}
        for start in range(0, len(keys), per_page)
    ] or [{}]


def _sheet_navigation(batch: str, page: int, total_pages: int, total_items: int) -> str:
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


def _probe_text(probe: object) -> str:
    """manifest に記録された ffprobe 要約を表示用文字列にする。"""
    if not isinstance(probe, dict):
        return "probe なし"
    return (
        f"{probe.get('width')}x{probe.get('height')} / {probe.get('fps')}fps / "
        f"{probe.get('duration')}s / video={probe.get('video_codec')} / "
        f"audio={probe.get('audio_codec')} {probe.get('sample_rate')}Hz "
        f"{probe.get('channels')}ch / valid={probe.get('valid')}"
    )


def _item_lookup(items: Iterable[dict[str, Any]] | Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """ストックを content_key で引ける形にする。"""
    if isinstance(items, Mapping):
        return {
            str(key): item for key, item in items.items() if isinstance(item, dict)
        }
    return {
        str(item["content_key"]): item
        for item in items
        if isinstance(item, dict) and item.get("content_key") is not None
    }


def generate_review_html(
    manifest: dict[str, Any],
    items: Iterable[dict[str, Any]] | Mapping[str, Any] = (),
    *,
    content_keys: Iterable[str] | None = None,
    base: Path = BASE,
    batch: str = "",
    page: int = 1,
    total_pages: int = 1,
    total_items: int | None = None,
) -> str:
    """manifest と素材から、エスケープ済みのバッチ別レビュー HTML を返す。

    素材を失った content_key も manifest の動画・静止画・probe を表示する。
    """
    item_by_key = _item_lookup(items)
    keys = list(content_keys) if content_keys is not None else sorted(manifest)
    missing = sorted(set(keys) - set(manifest))
    if missing:
        raise ValueError("manifest にない content_key です: " + ", ".join(missing))

    work_dir = base / "work"
    review_dir = work_dir / "review"
    navigation = _sheet_navigation(
        batch, page, total_pages, len(manifest) if total_items is None else total_items
    )
    provisional_count = sum(
        1
        for key in keys
        if _mapping(_mapping(manifest.get(key)).get("bgm")).get("provisional") is True
    )
    cards: list[str] = []
    for key in keys:
        record = manifest.get(key)
        if not isinstance(record, dict):
            record = {}
        item = item_by_key.get(str(record.get("content_key") or key))
        title = item.get("title") if item else "素材なし"
        video_value = record.get("video")
        video_url = _relative_asset(
            video_value, base=base, work_dir=work_dir, review_dir=review_dir
        )
        video_html = (
            f'<video controls loop preload="metadata" src="{_asset(video_url)}"></video>'
            if video_url else '<p class="missing-media">動画なし</p>'
        )
        stills = _mapping(record.get("stills"))
        still_html = "".join(
            f'<figure><img loading="lazy" src="{_asset(_relative_asset(path, base=base, work_dir=work_dir, review_dir=review_dir))}" '
            f'alt="{_asset(label)}"><figcaption>{_text(label)}</figcaption></figure>'
            for label, path in stills.items()
            if isinstance(path, str) and path
        )
        media_html = f'<div class="media">{video_html}<div class="stills">{still_html}</div></div>'
        probe_html = f"<p><b>ffprobe:</b> {_text(_probe_text(record.get('probe')))}</p>"

        if item is None:
            content_html = (
                '<p class="unclassified">stock_items.py に問題の素材がありません。'
                "manifest に記録された動画・静止画・probe を表示しています。</p>"
                + probe_html
            )
        else:
            bgm = _mapping(record.get("bgm"))
            narration = _mapping(record.get("narration"))
            timeline = _mapping(record.get("timeline"))
            lines = _mapping(item.get("character_lines"))
            master = _mapping(lines.get("master"))
            jr = _mapping(lines.get("jr"))
            play = item.get("play_example")
            play_html = "".join(
                f"<li><b>{_text(line.get('role'))}</b>: {_text(line.get('text'))}</li>"
                for line in play if isinstance(line, dict)
            ) if isinstance(play, list) else ""
            facts = item.get("fact_sheet")
            facts_html = "".join(
                f"<li>{_text(fact)}</li>" for fact in facts
            ) if isinstance(facts, list) else ""
            tempo_html = f" ×{_text(narration['tempo'])}" if narration.get("tempo") is not None else ""
            engine_html = f" / {_text(narration['engine_id'])}" if narration.get("engine_id") else ""
            if str(narration.get("engine_id", "")).startswith("irodori/"):
                if narration.get("seed") is not None and narration.get("seconds") is not None:
                    engine_html += f" (seed={_text(narration['seed'])}, seconds={_text(narration['seconds'])})"
            provisional = bgm.get("provisional") is True
            bgm_class = " provisional" if provisional else ""
            bgm_label = "暫定 BGM（publish 不可）" if provisional else "正式 BGM"
            timeline_html = (
                f"<p><b>タイムライン:</b> 導入 0–{_text(timeline.get('opening_end'))}f → 本編 "
                f"{_text(timeline.get('main_fully_visible'))}f で切替完了 / ナレーション 見出し "
                f"{_text(timeline.get('narration_opening_start'))}–{_text(timeline.get('narration_opening_end'))}f・problem "
                f"{_text(timeline.get('narration_problem_start'))}f・rule "
                f"{_text(timeline.get('narration_rule_start'))}f・終了 {_text(timeline.get('narration_end'))}f / 総 "
                f"{_text(timeline.get('total_frames'))}f</p>"
                if timeline else ""
            )
            content_html = (
                '<div class="copy">'
                f"<p><b>フック:</b> {_text(item.get('hook'))}</p>"
                f"<p><b>問題文:</b> {_text(item.get('problem_text'))}</p>"
                f"<p><b>ルール:</b> {_text(item.get('rule_text'))}</p>"
                f"<p><b>カメロック:</b> {_text(master.get('intro'))} / {_text(master.get('outro'))}<br>"
                f"<b>Jr.:</b> {_text(jr.get('outro'))}</p>"
                f"<ol>{play_html}</ol><p><b>キャプション:</b><br>{_text(item.get('caption'))}</p></div>"
                f'<p class="bgm{bgm_class}"><b>{_text(bgm_label)}:</b> '
                f"{_text(bgm.get('track'))} / {_text(bgm.get('s3_key'))}</p>"
                f"<p><b>ナレーション:</b> problem={_text(narration.get('problem_sec'))}s + "
                f"gap=1.2s + rule={_text(narration.get('rule_sec'))}s = "
                f"<b>{_text(narration.get('total_sec'))}s / 21.0s</b>{tempo_html}{engine_html}</p>"
                f"{probe_html}{timeline_html}"
                '<details><summary>真相・確定事実シート（レビュー時だけ開く）</summary>'
                f"<p>{_text(item.get('truth'))}</p><ul>{facts_html}</ul></details>"
            )
        cards.append(
            f'<section id="{_asset(key)}"><h2>{_text(key)} — {_text(title)}</h2>'
            f"{media_html}{content_html}</section>"
        )

    warning = (
        f'<p class="warning">警告: 暫定 BGM が {provisional_count} 件あります。'
        "正式トラックへ再選曲するまで publish できません。</p>"
        if provisional_count else '<p class="ok">暫定 BGM はありません。</p>'
    )
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>umigame-soup-1 動画レビュー</title><style>
body{{font-family:system-ui,sans-serif;background:#f1eee7;color:#24211d;margin:0;padding:20px;line-height:1.65}}
main{{max-width:1120px;margin:auto}}section{{background:white;padding:20px;margin:22px 0;border-radius:12px;box-shadow:0 2px 8px #0002}}
.media{{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}}video{{width:min(340px,100%);background:#111}}
.stills{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;flex:1;min-width:280px}}
figure{{margin:0}}figure img{{width:100%;aspect-ratio:9/16;object-fit:cover}}figcaption{{font-size:12px}}
.copy{{white-space:pre-wrap}}.bgm{{padding:8px;background:#edf7ed}}.provisional,.warning{{background:#ffe3df;color:#8b1e16;padding:10px;border:2px solid #c43}}
.ok{{background:#edf7ed;padding:10px}}details{{border-top:1px solid #ccc;padding-top:10px}}code{{background:#eee;padding:2px 4px}}
.unclassified,.missing-media{{color:#7a4c00;background:#fff6dc;padding:10px}}.pager{{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:#fff;padding:12px 16px;border-radius:10px;font-size:14px;margin:16px 0}}
.pager a,.pager .current{{padding:6px 12px;border-radius:6px;text-decoration:none}}.pager a{{background:#eef1f6;color:#1b2a4a}}.pager .current{{background:#1b2a4a;color:#fff}}
.sheet-navigation>p{{margin:12px 0}}
@media(max-width:600px){{body{{padding:10px}}section{{padding:14px}}.stills{{min-width:100%}}.pager a,.pager .current{{padding:12px 16px;min-height:44px;box-sizing:border-box}}}}
</style></head><body><main><h1>umigame-soup-1 事前動画レビュー: {_text(batch)}</h1>
<p>尺は {DURATION_SECONDS} 秒・一本道（先頭 5.0 秒が導入シーン）。レビュー観点: ①導入シーン（最初の 1 秒で「コメントで紐解く推理ゲーム」と伝わるか・hook が「今日の謎」のカードに 1 行で収まるか・自己紹介の吹き出し）
②導入 → 本編の切り替わり ③背景イラスト（文字混入、真相の手がかりを描いていないか、画風 C4、上部 55% が落ち着いているか）
④版面（見切れ、吹き出し 1 行） ⑤音（ナレーションと BGM のバランス、BGM の終わり方）。</p>
<p>承認した動画は <code>work/approved.txt</code> に 1 行 1 content_key で記入する。<code>#</code> から始まる行はコメントとして無視される。</p>
{warning}{navigation}{''.join(cards)}{navigation}</main></body></html>\n"""


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
    archive: dict[str, Any], seeds: Iterable[dict[str, Any]], current: dict[str, Any]
) -> dict[str, Any]:
    """既存台帳、seed の指定順、今回 manifest の順にマージする。"""
    merged = dict(archive)
    for manifest in seeds:
        merged.update(manifest)
    merged.update(current)
    return merged


def load_item_lookup(stock_root: Path) -> dict[str, tuple[str, dict[str, Any]]]:
    """全 batch-* の stock_items.py から content_key → (batch, item) を作る。"""
    lookup: dict[str, tuple[str, dict[str, Any]]] = {}
    if not stock_root.is_dir():
        return lookup
    canonical_root = DEFAULT_STOCK_ROOT.resolve()
    for batch_dir in sorted(stock_root.iterdir(), key=lambda path: path.name):
        if not batch_dir.is_dir() or not batch_dir.name.startswith("batch-"):
            continue
        stock_file = batch_dir / "stock_items.py"
        if not stock_file.is_file():
            continue
        try:
            if stock_root.resolve() == canonical_root:
                items = load_items(batch_dir.name)
            else:
                items = runpy.run_path(str(stock_file)).get("ITEMS")
            if not isinstance(items, list):
                raise ValueError("ITEMS が list ではありません")
            for item in items:
                if not isinstance(item, dict):
                    continue
                content_key = item.get("content_key")
                if isinstance(content_key, str) and content_key:
                    lookup[content_key] = (batch_dir.name, item)
        except Exception as exc:
            print(f"警告: バッチを読み込めません: {stock_file}: {exc}", file=sys.stderr)
    return lookup


def assign_batches(
    manifest: dict[str, Any],
    stock_root: Path,
    item_lookup: dict[str, tuple[str, dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """台帳の各レコードへ stock_items.py のバッチを割り当てる。"""
    lookup = item_lookup if item_lookup is not None else load_item_lookup(stock_root)
    assigned: dict[str, Any] = {}
    for key, value in manifest.items():
        if not isinstance(value, dict):
            assigned[key] = value
            continue
        record = dict(value)
        content_key = str(record.get("content_key") or key)
        record["batch"] = lookup.get(content_key, (UNCLASSIFIED, {}))[0]
        assigned[key] = record
    return assigned


def _record_video_paths(record: dict[str, Any], base: Path, work_dir: Path) -> list[Path]:
    """台帳レコードから動画パスを得る。"""
    path = _work_asset_path(record.get("video"), base=base, work_dir=work_dir)
    return [path] if path is not None else []


def _last_build_label(
    records: dict[str, Any], *, base: Path, work_dir: Path
) -> str:
    """バッチ内で最も新しい動画の mtime を JST 分単位で返す。"""
    timestamps = [
        path.stat().st_mtime
        for record in records.values()
        if isinstance(record, dict)
        for path in _record_video_paths(record, base, work_dir)
        if path.is_file()
    ]
    if not timestamps:
        return "—"
    latest = datetime.fromtimestamp(max(timestamps), timezone.utc).astimezone(JST)
    return latest.strftime("%Y-%m-%d %H:%M JST")


def generate_index_html(
    manifest: dict[str, Any],
    *,
    current_batch: str | None = None,
    per_page: int = 14,
    base: Path = BASE,
    work_dir: Path = WORK,
) -> str:
    """バッチ別シートへのリンクを持つレビューインデックスを返す。"""
    groups: dict[str, dict[str, Any]] = {}
    for key, record in manifest.items():
        if not isinstance(record, dict):
            continue
        batch = str(record.get("batch") or UNCLASSIFIED)
        groups.setdefault(batch, {})[key] = record

    total_items = sum(len(records) for records in groups.values())
    rows: list[str] = []
    for batch in sorted(groups, reverse=True):
        records = groups[batch]
        page_count = max(1, (len(records) + per_page - 1) // per_page)
        page_links = " ".join(
            f'<a href="review/{quote(sheet_page_name(batch, page))}">{page}ページ目</a>'
            for page in range(1, page_count + 1)
        )
        marker = ' <strong class="current">今回</strong>' if batch == current_batch else ""
        rows.append(
            "<tr>"
            f"<th>{escape(batch)}{marker}{UNCLASSIFIED_NOTE if batch == UNCLASSIFIED else ''}</th>"
            f"<td>{len(records)} 件</td>"
            f"<td>{escape(_last_build_label(records, base=base, work_dir=work_dir))}</td>"
            f"<td>{page_links}</td></tr>"
        )
    return """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>umigame-soup-1 レビューインデックス</title><style>
body{font-family:sans-serif;background:#f4f4f4;margin:24px;color:#222}
table{border-collapse:collapse;background:#fff;width:100%;margin-top:16px}
th,td{border:1px solid #ccc;padding:10px;text-align:left;vertical-align:top}
th{white-space:nowrap}.current{color:#a33;margin-left:8px}
a{margin-right:10px}.summary{font-size:18px}
@media(max-width:640px){body{margin:12px}th,td{padding:7px;font-size:13px}}
</style></head><body><h1>umigame-soup-1 レビューインデックス</h1>
<p class="summary">全体: """ + str(total_items) + """ 件</p>
<table><thead><tr><th>バッチ</th><th>件数</th><th>最終ビルド日時</th>
<th>シート</th></tr></thead><tbody>""" + "\n".join(rows) + """
</tbody></table></body></html>
"""


def _cleanup_outputs(work_dir: Path, review_dir: Path, expected: set[str]) -> None:
    """旧分割ファイルと今回生成しないバッチシートを削除する。"""
    for stale in work_dir.glob("review-*.html"):
        if re.fullmatch(r"review-\d+\.html", stale.name):
            stale.unlink()
    if not review_dir.exists():
        return
    for stale in review_dir.rglob("*.html"):
        if stale.relative_to(review_dir).as_posix() not in expected:
            stale.unlink()


def write_review(
    manifest: dict[str, Any] | None = None,
    *,
    batch: str | None = None,
    content_keys: Iterable[str] | None = None,
    output: Path | None = None,
    per_page: int = 14,
    seed_from: Iterable[Path] | None = None,
    stock_root: Path = DEFAULT_STOCK_ROOT,
) -> Path:
    """累積台帳を更新し、work/review.html とバッチ別シートを書く。"""
    if per_page <= 0:
        raise ValueError("--per-page は 1 以上にしてください")
    index_path = output or (WORK / "review.html")
    work_dir = index_path.parent
    current = _load_manifest(work_dir / "manifest.json", required=False) if manifest is None else manifest
    archive_path = work_dir / "review_archive.json"
    archive = _load_manifest(archive_path, required=False)
    seeds = load_seed_manifests(seed_from or [])
    merged = merge_manifests(archive, seeds, current)
    lookup = load_item_lookup(stock_root)
    merged = assign_batches(merged, stock_root, item_lookup=lookup)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    selected = dict(merged)
    if content_keys is not None:
        requested = list(dict.fromkeys(str(key) for key in content_keys))
        missing = sorted(set(requested) - set(merged))
        if missing:
            raise ValueError("manifest にない content_key です: " + ", ".join(missing))
        requested_set = set(requested)
        selected = {key: value for key, value in merged.items() if key in requested_set}

    groups: dict[str, dict[str, Any]] = {}
    for key, record in selected.items():
        if isinstance(record, dict):
            groups.setdefault(str(record.get("batch") or UNCLASSIFIED), {})[key] = record

    review_dir = work_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    expected: set[str] = set()
    outputs: list[tuple[Path, int]] = []
    for group_batch in sorted(groups, reverse=True):
        batch_manifest = groups[group_batch]
        pages = paginate(batch_manifest, per_page)
        batch_items = {
            str(record.get("content_key") or key): lookup.get(
                str(record.get("content_key") or key), (group_batch, {})
            )[1]
            for key, record in batch_manifest.items()
            if isinstance(record, dict)
            and str(record.get("content_key") or key) in lookup
        }
        for page_number, page_manifest in enumerate(pages, start=1):
            filename = sheet_page_name(group_batch, page_number)
            expected.add(filename)
            page_items = {
                key: item for key, item in batch_items.items()
                if any(
                    str(record.get("content_key") or content_key) == key
                    for content_key, record in page_manifest.items()
                    if isinstance(record, dict)
                )
            }
            sheet_path = review_dir / filename
            sheet_path.write_text(
                generate_review_html(
                    page_manifest,
                    page_items,
                    base=BASE,
                    batch=group_batch,
                    page=page_number,
                    total_pages=len(pages),
                    total_items=len(batch_manifest),
                ),
                encoding="utf-8",
            )
            outputs.append((sheet_path, len(page_manifest)))

    index_path.write_text(
        generate_index_html(
            selected, current_batch=batch, per_page=per_page,
            base=BASE, work_dir=work_dir,
        ),
        encoding="utf-8",
    )
    _cleanup_outputs(work_dir, review_dir, expected)
    print(f"インデックス: {index_path}（全 {len(selected)} 件）")
    for sheet_path, item_count in outputs:
        print(f"シート: {sheet_path}（{item_count} 件）")
    return index_path


def main(argv: list[str] | None = None) -> int:
    """累積台帳を更新し、インデックスとバッチ別シートを書き出す。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", help="今回ビルドしたバッチ（インデックスの印）")
    parser.add_argument("--content-key", action="append", dest="content_keys")
    parser.add_argument(
        "--per-page", type=int, default=14, metavar="N",
        help="1 シートあたりの動画数（既定 14）",
    )
    parser.add_argument(
        "--seed-from", nargs="+", type=Path, metavar="FILE",
        help="過去の manifest JSON を指定順に台帳へ追加する",
    )
    parser.add_argument(
        "--stock-root", type=Path, default=DEFAULT_STOCK_ROOT,
        help="バッチ判定に使う stock_items.py の親ディレクトリ",
    )
    args = parser.parse_args(argv)
    if args.per_page <= 0:
        parser.error("--per-page は 1 以上にしてください")
    try:
        write_review(
            batch=args.batch,
            content_keys=args.content_keys,
            per_page=args.per_page,
            seed_from=args.seed_from,
            stock_root=args.stock_root,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
