"""単色背景（imagegen が透過を無視して塗ったマゼンタ等）を抜いて透過 PNG にする（PIL。Docker で実行）。

四隅の色を背景色とみなし、色距離が threshold 未満の画素を透明に、threshold〜threshold*1.6 の画素は
線形にアルファを落とす（縁のハロー軽減）。使い方: key_out_background.py <in.png> <out.png> [threshold=90]
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


def main() -> int:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 90.0
    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    soft = threshold * 1.6
    keyed = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            d = ((r - bg[0]) ** 2 + (g - bg[1]) ** 2 + (b - bg[2]) ** 2) ** 0.5
            if d < threshold:
                px[x, y] = (0, 0, 0, 0)
                keyed += 1
            elif d < soft:
                px[x, y] = (r, g, b, int(a * (d - threshold) / (soft - threshold)))
    img.save(dst, "PNG", optimize=True)
    print(f"{src.name}: bg={bg} keyed {keyed / (w * h):.1%} -> {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
