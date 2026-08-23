"""Create a local HTML sheet for all prebuilt-video review candidates."""

from __future__ import annotations

from html import escape

from common import WORK, load_json


def main() -> None:
    """Write an HTML page containing video, illustration, and cut previews."""
    manifest = load_json(WORK / "build_manifest.json", {})
    cards: list[str] = []
    for stock_id in sorted(manifest, key=int):
        record = manifest[stock_id]
        # カット枚数はレンダラーの構成で変わるため、実ファイルから数える
        cut_paths = sorted((WORK / "cuts").glob(f"{stock_id}_cut*.png"))
        cuts = "".join(
            f'<img src="cuts/{path.name}" alt="{escape(path.stem)}">'
            for path in cut_paths
        )
        slot_code = escape(str(record.get("slot_code", "")))
        content_key = escape(str(record.get("content_key", "")))
        question = escape(str(record.get("question_text", "")))
        cards.append(
            f"<section><h2>stock_item_id: {escape(stock_id)}"
            f'<span class="slot">{content_key or slot_code}</span></h2>'
            f'<p class="question">{question}</p>'
            f'<video controls src="videos/{escape(stock_id)}.mp4"></video>'
            f'<img class="illustration" src="illustrations/{escape(stock_id)}.png" '
            f'alt="illustration {escape(stock_id)}"><div class="cuts">{cuts}</div></section>'
        )
    html = """<!doctype html><meta charset="utf-8"><title>Prebuilt video review</title>
<style>body{font-family:sans-serif;background:#f4f4f4;margin:24px}section{background:white;padding:16px;margin:16px 0;border-radius:8px}video{width:270px;max-height:480px;background:#111}.illustration{width:360px;display:block;margin:12px 0}.cuts{display:flex;gap:8px}.cuts img{width:160px}
h2{font-size:16px;margin:0}.slot{margin-left:8px;padding:2px 8px;border-radius:10px;background:#e8eef5;font-size:12px;font-weight:normal}
.question{margin:8px 0 0;font-size:14px;color:#333}</style>
<h1>logic-training-1 prebuilt video review</h1><p>全数確認: 文字・数字・記号混入、画風、情景適合、版面、音。</p>""" + "\n".join(cards)
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "review.html").write_text(html, encoding="utf-8")
    print(f"wrote {WORK / 'review.html'}")


if __name__ == "__main__":
    main()
