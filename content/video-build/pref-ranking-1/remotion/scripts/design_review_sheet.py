"""17-4a 版面デザイン工程のレビューシートを生成する。

work/out/ にレンダリング済みの静止画（{name}_{frame}.png）と 20 秒モック
（{name}_20s_mock.mp4）を並べた HTML を work/design-review.html に書き出す。

    python scripts/design_review_sheet.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "work" / "design-review.html"

FRAMES = [
    (0, "0:00 開幕。タイトル・地図・全国平均を最初から出す"),
    (100, "0:03 煽り。吹き出しは teaser から"),
    (180, "0:06 5 位確定。県名が行へ落ちる"),
    (310, "0:10 3 位確定"),
    (470, "0:15 1 位発表"),
    (575, "0:19 締め。TOP5 総覧"),
]
EDGE_FRAMES = [
    (170, "5 位 = 鹿児島（発表直後）"),
    (180, "5 位 = 鹿児島（県名が飛ぶ）"),
    (340, "2 位 = 沖縄（インセット）"),
]

STYLE = """
body { font-family: sans-serif; background:#20242e; color:#e8e6df; margin:0; padding:28px; }
h1 { font-size:20px; margin:0 0 6px; } p.note { color:#a8a49a; font-size:13px; margin:0 0 22px; }
h2 { font-size:16px; margin:32px 0 10px; border-left:5px solid #D9A62E; padding-left:10px; }
.row { display:flex; gap:22px; flex-wrap:wrap; }
.row figure { margin:0; }
video { width:300px; border-radius:10px; background:#000; }
img { width:250px; border-radius:8px; display:block; }
figcaption { font-size:13px; color:#c9c5bb; margin-top:6px; max-width:250px; }
"""


def figure(src: str, caption: str, video: bool = False) -> str:
    media = (
        f'<video src="{src}" controls muted loop></video>'
        if video
        else f'<img src="{src}">'
    )
    return f"<figure>{media}<figcaption>{caption}</figcaption></figure>"


def main() -> None:
    keyframes = "".join(figure(f"out/main_{f}.png", label) for f, label in FRAMES)
    edge = "".join(figure(f"out/edge_{f}.png", label) for f, label in EDGE_FRAMES)

    DEST.write_text(
        "<!doctype html><html lang='ja'><head><meta charset='utf-8'>"
        "<title>17-4a 版面デザイン レビュー</title>"
        f"<style>{STYLE}</style></head><body>"
        "<h1>17-4a 版面デザイン（生成り地 × 淡墨茶 × 金で Fix）</h1>"
        "<p class='note'>ネタは 001 ぎょうざ。ナレーション・BGM は未搭載（17-4d）。"
        "キャラ・地図・フォントは仮素材（正式化は 17-4b）。</p>"
        "<h2>20 秒通し</h2><div class='row'>"
        + figure("out/main_20s_mock.mp4", "通常ネタ（001 ぎょうざ）", video=True)
        + figure(
            "out/edge_20s_mock.mp4",
            "端の県の検証（5 位 = 鹿児島 / 2 位 = 沖縄 / 1 位 = 北海道）",
            video=True,
        )
        + "</div>"
        f"<h2>キーフレーム</h2><div class='row'>{keyframes}</div>"
        f"<h2>端の県が隠れないかの検証</h2><div class='row'>{edge}</div>"
        "</body></html>",
        encoding="utf-8",
    )
    print(f"wrote {DEST}")


if __name__ == "__main__":
    main()
