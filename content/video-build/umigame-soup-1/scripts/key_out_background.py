"""imagegen が透過を無視して塗った背景を抜いて透過 PNG にする（PIL のみ。Docker で実行）。

imagegen は透過指定を無視して単色（マゼンタ等）やノイズ状の彩度の高い背景を返すことがある
（21-2 第 2 稿の Jr. で 2 回発生）。四隅の 1 色だけを見る単純なキーではノイズ背景を抜けないため、

  1. 外周の画素から代表色（量子化して出現率の高い色）を数色拾う。彩度の低い色は除く
     （黒い輪郭線を背景色に含めるとキャラの中まで抜けてしまう）
  2. どれかの代表色に近い画素を「背景候補」とする
  3. 背景候補のうち **画像の外周とつながっている領域だけ** を透明にする
     （キャラ内部の同系色〔緑の肌など〕を誤って抜かないため。輪郭線が濃いので漏れにくい）
  4. 縁 1〜2 画素はアルファを段階的に落としてハローを減らす

使い方: key_out_background.py <in.png> <out.png> [threshold=110]
"""

from __future__ import annotations

import sys
from collections import Counter, deque
from pathlib import Path

from PIL import Image

QUANT = 24  # 代表色を拾うときの量子化幅


def border_palette(px, w: int, h: int, band: int = 3) -> list[tuple[int, int, int]]:
    counter: Counter = Counter()
    for y in range(h):
        for x in range(w):
            if x >= band and x < w - band and y >= band and y < h - band:
                continue
            r, g, b, _ = px[x, y]
            counter[(r // QUANT, g // QUANT, b // QUANT)] += 1
    total = sum(counter.values())
    palette = []
    for key, count in counter.most_common(12):
        if count / total < 0.03:
            continue
        color = tuple(int(c * QUANT + QUANT / 2) for c in key)
        # 彩度の低い色（黒い輪郭線・白い小物）は背景色とみなさない。これを入れるとキャラの
        # 輪郭ごと抜けて内部へ漏れる（21-2 第 2 稿の Jr. で実際に起きた）
        if max(color) - min(color) < 60 or max(color) < 60:
            continue
        palette.append(color)
    return palette


def main() -> int:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 110.0
    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size

    palette = border_palette(px, w, h)
    if not palette:
        raise SystemExit("外周から背景の代表色を拾えませんでした")
    soft = threshold * 1.5

    def distance(r: int, g: int, b: int) -> float:
        return min(
            ((r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2) ** 0.5 for pr, pg, pb in palette
        )

    # 背景候補（代表色に近い）を判定しつつ、外周からの塗りつぶしで連結成分だけを抜く
    visited = bytearray(w * h)
    queue: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            queue.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            queue.append((x, y))

    keyed = 0
    while queue:
        x, y = queue.popleft()
        index = y * w + x
        if visited[index]:
            continue
        visited[index] = 1
        r, g, b, a = px[x, y]
        d = distance(r, g, b)
        if d >= soft:
            continue
        if d < threshold:
            px[x, y] = (0, 0, 0, 0)
            keyed += 1
        else:
            px[x, y] = (r, g, b, int(a * (d - threshold) / (soft - threshold)))
            continue  # 半透明の縁で伝播を止める
        if x > 0:
            queue.append((x - 1, y))
        if x < w - 1:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y < h - 1:
            queue.append((x, y + 1))

    img.save(dst, "PNG", optimize=True)
    print(f"{src.name}: palette={palette} keyed {keyed / (w * h):.1%} -> {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
