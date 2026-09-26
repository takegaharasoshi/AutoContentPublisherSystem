"""背景イラストだけを投稿順に並べたレビュー用 HTML を生成する（動画の再ビルド前に背景を見るため）。

出力は ``work/backgrounds.html``。問題文・フック・scene を背景の横に並べ、真相は折りたたんで
「真相の手がかりが背景に出ていないか」を照合できるようにする。
"""

from __future__ import annotations

import argparse
import importlib.util
from html import escape
from pathlib import Path
from typing import Any

from common import WORK, _stock_path, load_items


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
            f"<p>{_text(item.get('truth'))}</p></details></div></div></section>"
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
    args = parser.parse_args(argv)
    try:
        html = generate_background_html(load_items(args.batch), _post_order(args.batch))
    except (OSError, ValueError) as exc:
        print(f"エラー: {exc}")
        return 1
    args.output.write_text(html, encoding="utf-8")
    print(f"背景レビューシートを書き出しました: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
