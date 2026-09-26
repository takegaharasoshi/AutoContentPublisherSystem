"""背景イラストだけを投稿順に並べたレビュー用 HTML を生成する（動画の再ビルド前に背景を見るため）。

出力は ``work/backgrounds.html``。問題文・フック・scene を背景の横に並べ、真相は折りたたんで
「真相の手がかりが背景に出ていないか」を照合できるようにする。

``--stills`` を付けると、今のストックの文言と今の背景で動画の各コマ（``build.STILL_FRAMES``）を
Remotion の ``renderStill`` で書き出し（``work/bgstills/``）、問題カード・キャラ・吹き出しとの重なりも見られるようにする。
ナレーションと BGM は静止画に影響しないため、合成も選曲もしない。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from html import escape
from pathlib import Path
from typing import Any

from build import (
    ASSETS_DIR, PUBLIC_DIR, REMOTION_DIR, REMOTION_IMAGE, STILL_FRAMES,
    _container_path, _docker, build_props,
)
from common import WORK, _stock_path, load_items, select_items, write_json

STILLS_DIR = WORK / "bgstills"


def _text(value: object) -> str:
    return escape(str(value if value is not None else ""))


def _post_order(batch: str) -> list[str]:
    """``stock_items.py`` の ``POST_ORDER``（問番号の並び）を返す。"""
    path = _stock_path(batch)
    spec = importlib.util.spec_from_file_location("umigame_post_order", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"ストックを読み込めません: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    order = getattr(module, "POST_ORDER", None)
    if not isinstance(order, list):
        raise ValueError(f"POST_ORDER がありません: {path}")
    return [str(no) for no in order]


def _scene(prompt: str) -> str:
    """illustration_prompt から Scene 部分だけを取り出す。"""
    for block in prompt.split("\n\n"):
        if block.startswith("Scene: "):
            return block[len("Scene: "):]
    return prompt


def render_stills(items: list[dict[str, Any]]) -> list[str]:
    """背景がある問について、各コマの静止画を ``work/bgstills/<key>_<label>.jpg`` に書き出す。"""
    design = json.loads((ASSETS_DIR / "design.json").read_text(encoding="utf-8"))
    for directory in (PUBLIC_DIR / "bg", PUBLIC_DIR / "char", STILLS_DIR / "props"):
        directory.mkdir(parents=True, exist_ok=True)
    for name in ("master_base", "master_happy", "jr_base"):
        shutil.copy2(ASSETS_DIR / "characters" / f"{name}.png", PUBLIC_DIR / "char" / f"{name}.png")
    # 静止画に音は出ないので、実在する効果音を仮のナレーション・BGM として渡す（長さは予算内の仮値）
    report = {"cues": {cue: {"seconds": 5.0, "frames": 150} for cue in ("problem", "rule")}}
    job_items: list[dict[str, str]] = []
    for item in items:
        key = str(item["content_key"])
        background = WORK / "backgrounds" / f"{key}.jpg"
        if not background.is_file():
            continue
        shutil.copy2(background, PUBLIC_DIR / "bg" / f"{key}.jpg")
        props = build_props(item, design, report, {"output": "unused"})
        props["bgm"] = "audio/se_pop.wav"
        for cue in ("problem", "rule"):
            props["narration"][cue]["file"] = "audio/se_pop.wav"
        props_path = STILLS_DIR / "props" / f"{key}.json"
        write_json(props_path, props)
        job_items.append(
            {"props": _container_path(props_path), "out": _container_path(STILLS_DIR / key)}
        )
    job_path = STILLS_DIR / "job.json"
    write_json(job_path, {"frames": STILL_FRAMES, "items": job_items})
    _docker(REMOTION_IMAGE, REMOTION_DIR, ["node", "scripts/render_stills.mjs", _container_path(job_path)])
    return [Path(entry["out"]).name for entry in job_items]


def _stills_html(key: str, background: Path) -> str:
    """その問の静止画の並び。背景より古い静止画は「古い」と表示する。"""
    figures: list[str] = []
    for label in STILL_FRAMES:
        still = STILLS_DIR / f"{key}_{label}.jpg"
        if not still.is_file():
            continue
        stale = background.is_file() and still.stat().st_mtime < background.stat().st_mtime
        src = escape(f"bgstills/{key}_{label}.jpg?v={int(still.stat().st_mtime)}", quote=True)
        mark = '<span class="stale">古い</span> ' if stale else ""
        figures.append(
            f'<figure><a href="{src}"><img loading="lazy" src="{src}" alt="{_text(label)}"></a>'
            f"<figcaption>{mark}{_text(label)}</figcaption></figure>"
        )
    if not figures:
        return '<p class="scene">コマの静止画なし（<code>background_sheet.py --stills</code> で生成）</p>'
    return f'<div class="stills">{"".join(figures)}</div>'


def generate_background_html(items: list[dict[str, Any]], order: list[str]) -> str:
    """外部依存のない背景レビュー HTML を返す。"""
    by_no = {str(item["no"]): item for item in items}
    missing = [no for no in order if no not in by_no]
    if missing:
        raise ValueError("POST_ORDER にあって ITEMS にない問: " + ", ".join(missing))
    cards: list[str] = []
    for index, no in enumerate(order, start=1):
        item = by_no[no]
        key = str(item["content_key"])
        image = WORK / "backgrounds" / f"{key}.jpg"
        if image.is_file():
            src = f"backgrounds/{key}.jpg?v={int(image.stat().st_mtime)}"
            media = f'<a href="{escape(src, quote=True)}"><img src="{escape(src, quote=True)}" alt="{_text(key)}"></a>'
        else:
            media = '<div class="none">背景なし（未生成）</div>'
        cards.append(
            f'<section id="{_text(no)}"><h2>{index}. {_text(no)} {_text(item.get("title"))}'
            f' <small>{_text(key)} / {_text(item.get("puzzle_type"))}</small></h2>'
            f'<label class="done"><input type="checkbox" data-key="{_text(key)}"> 確認済み</label>'
            f'<div class="row"><div class="media">{media}</div><div class="copy">'
            f"<p><b>フック:</b> {_text(item.get('hook'))}</p>"
            f"<p><b>問題文:</b> {_text(item.get('problem_text'))}</p>"
            f'<p><b>scene:</b> <span class="scene">{_text(_scene(str(item.get("illustration_prompt", ""))))}</span></p>'
            "<details><summary>真相（手がかりの照合用）</summary>"
            f"<p>{_text(item.get('truth'))}</p></details></div></div>"
            f"{_stills_html(key, image)}</section>"
        )
    nav = " ".join(f'<a href="#{_text(no)}">{_text(no)}</a>' for no in order)
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>umigame-soup-1 背景レビュー</title><style>
body{{font-family:system-ui,sans-serif;background:#f1eee7;color:#24211d;margin:0;padding:20px;line-height:1.65}}
main{{max-width:1120px;margin:auto}}nav{{position:sticky;top:0;background:#f1eee7;padding:6px 0;z-index:1;font-size:14px}}
nav a{{margin-right:8px}}section{{background:white;padding:20px;margin:22px 0;border-radius:12px;box-shadow:0 2px 8px #0002}}
h2 small{{font-weight:normal;font-size:13px;color:#666}}.row{{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}}
.media{{width:min(360px,100%)}}.media img{{width:100%;aspect-ratio:9/16;object-fit:cover;display:block;border-radius:6px}}
.none{{aspect-ratio:9/16;display:grid;place-items:center;background:#ddd;border-radius:6px}}
.copy{{flex:1;min-width:260px}}.scene{{font-size:14px;color:#444}}.done{{display:block;margin-bottom:8px}}
.stills{{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:14px}}
.stills figure{{margin:0}}.stills img{{width:100%;aspect-ratio:9/16;object-fit:cover;display:block}}
.stills figcaption{{font-size:12px}}.stale{{background:#ffe3df;color:#8b1e16;padding:0 4px}}
details{{border-top:1px solid #ccc;padding-top:8px}}
@media(max-width:600px){{body{{padding:10px}}section{{padding:14px}}}}
</style></head><body><main><h1>umigame-soup-1 背景レビュー</h1>
<p>投稿順（POST_ORDER）。観点: 文字の混入 / 真相の手がかりを描いていないか / 問題文との食い違い / 画風 C4 / 上部 55% が落ち着いているか。画像を押すと原寸。</p>
<nav>{nav}</nav>{''.join(cards)}</main>
<script>
document.querySelectorAll('input[data-key]').forEach(function (box) {{
  var k = 'bgdone:' + box.dataset.key;
  try {{ box.checked = localStorage.getItem(k) === '1'; }} catch (e) {{}}
  box.addEventListener('change', function () {{
    try {{ localStorage.setItem(k, box.checked ? '1' : '0'); }} catch (e) {{}}
  }});
}});
</script></body></html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", default="batch-01")
    parser.add_argument("--output", type=Path, default=WORK / "backgrounds.html")
    parser.add_argument("--stills", action="store_true", help="各コマの静止画も Remotion で書き出す")
    parser.add_argument(
        "--content-key", action="append", dest="content_keys", help="--stills の対象（既定: 全問）"
    )
    args = parser.parse_args(argv)
    try:
        if args.stills:
            targets = select_items(load_items(args.batch), args.content_keys)
            print(f"{len(render_stills(targets))} 問の静止画を書き出しました: {STILLS_DIR}")
        html = generate_background_html(load_items(args.batch), _post_order(args.batch))
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"エラー: {exc}")
        return 1
    args.output.write_text(html, encoding="utf-8")
    print(f"背景レビューシートを書き出しました: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
