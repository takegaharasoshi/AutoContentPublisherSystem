"""Create a local HTML sheet for all prebuilt-video review candidates."""

from __future__ import annotations

from html import escape

from common import WORK, load_json


def main() -> None:
    """Write an HTML page containing video, illustration, and cut previews."""
    manifest = load_json(WORK / "build_manifest.json", {})
    cards: list[str] = []
    for stock_id in sorted(manifest, key=int):
        cuts = "".join(
            f'<img src="cuts/{stock_id}_cut{index}.png" alt="cut {index}">' 
            for index in range(1, 5)
        )
        cards.append(
            f"<section><h2>stock_item_id: {escape(stock_id)}</h2>"
            f'<video controls src="videos/{escape(stock_id)}.mp4"></video>'
            f'<img class="illustration" src="illustrations/{escape(stock_id)}.png" '
            f'alt="illustration {escape(stock_id)}"><div class="cuts">{cuts}</div></section>'
        )
    html = """<!doctype html><meta charset="utf-8"><title>Prebuilt video review</title>
<style>body{font-family:sans-serif;background:#f4f4f4;margin:24px}section{background:white;padding:16px;margin:16px 0;border-radius:8px}video{width:270px;max-height:480px;background:#111}.illustration{width:360px;display:block;margin:12px 0}.cuts{display:flex;gap:8px}.cuts img{width:160px}</style>
<h1>logic-training-1 prebuilt video review</h1><p>全数確認: 文字・数字・記号混入、画風、情景適合、版面、音。</p>""" + "\n".join(cards)
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "review.html").write_text(html, encoding="utf-8")
    print(f"wrote {WORK / 'review.html'}")


if __name__ == "__main__":
    main()
