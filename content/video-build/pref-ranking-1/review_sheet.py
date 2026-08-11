"""ビルド台帳から全数レビュー用 HTML を生成する。"""

from __future__ import annotations

import argparse
from html import escape
import os
from pathlib import Path
from typing import Any

from common import BASE, DURATIONS, WORK, load_json


def _relative_asset(path: Path, work: Path) -> str:
    """review.html から参照できる URL 形式の相対パスを返す。"""
    return Path(os.path.relpath(path, work)).as_posix()


def _display_value(value: Any, props: dict[str, Any]) -> str:
    """順位行に出るのと同じ整形（前置き + 桁区切り + 単位）を返す。

    生値だけだと「年間3,478円」と読ませたい表示が正しいかを判断できないため、
    レビューでは版面と同じ文字列を並べて見せる（版面側の整形は
    ``PrefRankingVideo.tsx`` の ``formatValue``）。
    """
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


def generate_review_html(manifest: dict[str, Any], *, base: Path = BASE) -> str:
    """manifest と尺別 props から HTML 文字列を生成する。"""
    work = base / "work"
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
            video_path = Path(video_value)
            if not video_path.is_absolute():
                video_path = base / video_path
            cue_items = "".join(
                f"<li><code>{escape(str(cue_id))}</code> "
                f"{escape(str(cue.get('text', '')))}</li>"
                for cue_id, cue in props.get("cues", {}).items()
                if isinstance(cue, dict)
            )
            loudness_i = escape(str(detail.get("loudness_i", "")))
            loudness_tp = escape(str(detail.get("loudness_tp", "")))
            duration_blocks.append(
                f'<div class="duration"><h3>{escape(duration)}</h3>'
                '<video controls preload="metadata" '
                f'src="{escape(_relative_asset(video_path, work), quote=True)}">'
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
            f'src="{escape(_relative_asset(background, work), quote=True)}" '
            f'alt="背景 {escape(content_key, quote=True)}"></div></div>'
            f"<table>{field_rows}</table><h3>TOP5</h3>"
            "<table><tr><th>順位</th><th>都道府県</th><th>値</th>"
            f"<th>版面表示</th></tr>{entries}</table>"
            f"<p>BGM: audio_asset_id={escape(str(record.get('audio_asset_id', '')))} / "
            f"s3_key={escape(str(record.get('bgm_s3_key', '')))}</p></section>"
        )
    return """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<title>pref-ranking-1 動画レビュー</title><style>
body{font-family:sans-serif;background:#f3f1eb;margin:24px;color:#222}
section{background:#fff;padding:20px;margin:20px 0;border-radius:10px}
.media{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}
.duration{width:300px}video{width:270px;max-height:480px;background:#111}
.background{width:270px;max-height:480px;object-fit:cover}
table{border-collapse:collapse;margin:12px 0}
th,td{border:1px solid #ccc;padding:6px 10px;text-align:left}
.cues{padding-left:24px;font-size:14px}code{font-weight:bold}
</style></head><body><h1>pref-ranking-1 事前動画レビュー</h1>
<p>全数・両尺を確認する。①背景イラストの品質（文字・数字・記号の混入、
和モダン調、版面の可読性） ②版面（県名・数値、金の可読性、見切れ、
地図と順位の整合） ③音（ナレーション同期、語尾切れ、BGM とのバランス）。</p>
""" + "\n".join(cards) + "</body></html>\n"


def main(argv: list[str] | None = None) -> int:
    """work/build_manifest.json から work/review.html を書き出す。"""
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    manifest = load_json(WORK / "build_manifest.json", {})
    if not isinstance(manifest, dict):
        raise RuntimeError("work/build_manifest.json は JSON オブジェクトにしてください")
    output = WORK / "review.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generate_review_html(manifest), encoding="utf-8")
    print(f"レビューシートを書き出しました: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
