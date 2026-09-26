"""manifest とストックから全数レビュー用 HTML を生成する。"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
from typing import Any, Iterable

from common import WORK, load_items, load_manifest, select_items


def _text(value: object) -> str:
    return escape(str(value if value is not None else ""))


def _asset(value: object) -> str:
    return escape(str(value if value is not None else ""), quote=True)


def _probe_text(probe: object) -> str:
    if not isinstance(probe, dict):
        return "probe なし"
    return (
        f"{probe.get('width')}x{probe.get('height')} / {probe.get('fps')}fps / "
        f"{probe.get('duration')}s / video={probe.get('video_codec')} / "
        f"audio={probe.get('audio_codec')} {probe.get('sample_rate')}Hz "
        f"{probe.get('channels')}ch / valid={probe.get('valid')}"
    )


def generate_review_html(
    manifest: dict[str, Any],
    items: Iterable[dict[str, Any]],
    *,
    content_keys: Iterable[str] | None = None,
) -> str:
    """外部依存のないレビュー HTML を返す。"""
    item_by_key = {str(item["content_key"]): item for item in items}
    keys = list(content_keys) if content_keys is not None else sorted(manifest)
    missing = sorted(set(keys) - set(manifest))
    if missing:
        raise ValueError("manifest にない content_key です: " + ", ".join(missing))
    provisional_count = sum(
        1
        for key in keys
        if isinstance(manifest.get(key), dict)
        and isinstance(manifest[key].get("bgm"), dict)
        and manifest[key]["bgm"].get("provisional") is True
    )
    cards: list[str] = []
    for key in keys:
        record = manifest.get(key)
        item = item_by_key.get(key)
        if not isinstance(record, dict) or not isinstance(item, dict):
            continue
        bgm = record.get("bgm") if isinstance(record.get("bgm"), dict) else {}
        narration = (
            record.get("narration") if isinstance(record.get("narration"), dict) else {}
        )
        tempo_html = (
            f" ×{_text(narration['tempo'])}"
            if narration.get("tempo") is not None else ""
        )
        engine_html = (
            f" / {_text(narration['engine_id'])}"
            if narration.get("engine_id") else ""
        )
        if str(narration.get("engine_id", "")).startswith("irodori/"):
            if narration.get("seed") is not None and narration.get("seconds") is not None:
                engine_html += (
                    f" (seed={_text(narration['seed'])}, "
                    f"seconds={_text(narration['seconds'])})"
                )
        provisional = bgm.get("provisional") is True
        bgm_class = " provisional" if provisional else ""
        bgm_label = "暫定 BGM（publish 不可）" if provisional else "正式 BGM"
        stills = record.get("stills") if isinstance(record.get("stills"), dict) else {}
        still_html = "".join(
            f'<figure><img loading="lazy" src="{_asset(path)}" alt="{_asset(label)}">'
            f"<figcaption>{_text(label)}</figcaption></figure>"
            for label, path in stills.items()
        )
        play_html = "".join(
            f"<li><b>{_text(line.get('role'))}</b>: {_text(line.get('text'))}</li>"
            for line in item.get("play_example", [])
            if isinstance(line, dict)
        )
        facts_html = "".join(
            f"<li>{_text(fact)}</li>" for fact in item.get("fact_sheet", [])
        )
        lines = item.get("character_lines", {})
        master = lines.get("master", {}) if isinstance(lines, dict) else {}
        jr = lines.get("jr", {}) if isinstance(lines, dict) else {}
        cards.append(
            f'<section id="{_asset(key)}"><h2>{_text(key)} — {_text(item.get("title"))}</h2>'
            '<div class="media">'
            f'<video controls loop preload="metadata" src="{_asset(record.get("video"))}"></video>'
            f'<div class="stills">{still_html}</div></div>'
            '<div class="copy">'
            f"<p><b>フック:</b> {_text(item.get('hook'))}</p>"
            f"<p><b>問題文:</b> {_text(item.get('problem_text'))}</p>"
            f"<p><b>ルール:</b> {_text(item.get('rule_text'))}</p>"
            f"<p><b>カメロック:</b> {_text(master.get('intro'))} / {_text(master.get('outro'))}<br>"
            f"<b>Jr.:</b> {_text(jr.get('outro'))}</p>"
            f"<ol>{play_html}</ol>"
            f"<p><b>キャプション:</b><br>{_text(item.get('caption'))}</p></div>"
            f'<p class="bgm{bgm_class}"><b>{_text(bgm_label)}:</b> '
            f"{_text(bgm.get('track'))} / {_text(bgm.get('s3_key'))}</p>"
            f"<p><b>ナレーション:</b> problem={_text(narration.get('problem_sec'))}s + "
            f"gap=1.2s + rule={_text(narration.get('rule_sec'))}s = "
            f"<b>{_text(narration.get('total_sec'))}s / 21.0s</b>"
            f"{tempo_html}{engine_html}</p>"
            f"<p><b>ffprobe:</b> {_text(_probe_text(record.get('probe')))}</p>"
            f"<p><b>継ぎ目平均差分:</b> {_text(record.get('seam_mean_diff'))} / 3.0 以下</p>"
            '<details><summary>真相・確定事実シート（レビュー時だけ開く）</summary>'
            f"<p>{_text(item.get('truth'))}</p><ul>{facts_html}</ul></details></section>"
        )
    warning = (
        f'<p class="warning">警告: 暫定 BGM が {provisional_count} 件あります。'
        "正式トラックへ再選曲するまで publish できません。</p>"
        if provisional_count
        else '<p class="ok">暫定 BGM はありません。</p>'
    )
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>umigame-soup-1 動画レビュー</title><style>
body{{font-family:system-ui,sans-serif;background:#f1eee7;color:#24211d;margin:0;padding:20px;line-height:1.65}}
main{{max-width:1120px;margin:auto}}section{{background:white;padding:20px;margin:22px 0;border-radius:12px;box-shadow:0 2px 8px #0002}}
.media{{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}}video{{width:min(340px,100%);background:#111}}
.stills{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;flex:1;min-width:280px}}
figure{{margin:0}}figure img{{width:100%;aspect-ratio:9/16;object-fit:cover}}figcaption{{font-size:12px}}
.copy{{white-space:pre-wrap}}.bgm{{padding:8px;background:#edf7ed}}.provisional,.warning{{background:#ffe3df;color:#8b1e16;padding:10px;border:2px solid #c43}}
.ok{{background:#edf7ed;padding:10px}}details{{border-top:1px solid #ccc;padding-top:10px}}code{{background:#eee;padding:2px 4px}}
@media(max-width:600px){{body{{padding:10px}}section{{padding:14px}}.stills{{min-width:100%}}}}
</style></head><body><main><h1>umigame-soup-1 動画レビュー</h1>
<p>レビュー観点: ①背景イラスト（文字混入、真相の手がかりを描いていないか、画風 C4、上部 55% が落ち着いているか）
②版面（見切れ、吹き出し 1 行） ③音（ナレーションと BGM のバランス、ループ継ぎ目）。</p>
<p>承認した動画は <code>work/approved.txt</code> に 1 行 1 content_key で記入する。<code>#</code> から始まる行はコメントとして無視される。</p>
{warning}{''.join(cards)}</main></body></html>
"""


def write_review(
    manifest: dict[str, Any] | None = None,
    *,
    batch: str = "batch-01",
    content_keys: Iterable[str] | None = None,
    output: Path = WORK / "review.html",
) -> Path:
    """対象を読み込んで work/review.html を書く。"""
    data = load_manifest() if manifest is None else manifest
    items = load_items(batch)
    selected_keys = list(content_keys) if content_keys is not None else None
    if selected_keys is not None:
        select_items(items, selected_keys)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        generate_review_html(data, items, content_keys=selected_keys), encoding="utf-8"
    )
    print(f"レビューシートを書き出しました: {output}")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", default="batch-01")
    parser.add_argument("--content-key", action="append", dest="content_keys")
    args = parser.parse_args(argv)
    try:
        write_review(batch=args.batch, content_keys=args.content_keys)
    except (OSError, ValueError) as exc:
        print(f"エラー: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
