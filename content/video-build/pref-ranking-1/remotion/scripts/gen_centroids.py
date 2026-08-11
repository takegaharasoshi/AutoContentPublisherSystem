"""japanPaths.ts の各県 bbox 中心を viewBox 座標へ換算し prefCentroids.ts を生成する。

地図 SVG を差し替えたら再実行する（確定県ラベルの表示位置に使う）。

    python scripts/gen_centroids.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src" / "japanPaths.ts"
DEST = Path(__file__).resolve().parent.parent / "src" / "prefCentroids.ts"

# 沖縄インセットの移設トランスフォーム（JapanMap.tsx の OKINAWA_INSET_TRANSFORM と同値）
OKINAWA_INSET = (695.0, 822.0, 0.75)
# OUTER_TRANSFORM の matrix スケール・オフセットと INNER_TRANSFORM の translate
OUTER_SCALE = 1.028807
OUTER_OFFSET = (-47.544239, -28.806583)
INNER_OFFSET = (6.0, 18.0)


def raw_points(fragment: str) -> list[tuple[float, float]]:
    """path の d / polygon の points から座標列を取り出す（絶対 M/L/Z のみ前提）。"""
    points: list[tuple[float, float]] = []
    for d in re.findall(r'd="([^"]+)"', fragment):
        nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", d)]
        points += list(zip(nums[0::2], nums[1::2]))
    for pts in re.findall(r'points="([^"]+)"', fragment):
        nums = [float(v) for v in pts.split()]
        points += list(zip(nums[0::2], nums[1::2]))
    return points


def shape_points(shapes: str) -> list[tuple[float, float]]:
    """飛び地のネスト <g transform> を展開して座標列を返す。"""
    points: list[tuple[float, float]] = []
    for match in re.finditer(r'<g transform="([^"]+)">(.*?)</g>', shapes, re.S):
        transform, inner = match.group(1), match.group(2)
        translate = re.search(r"translate\(([-\d.]+)[ ,]+([-\d.]+)\)", transform)
        scale = re.search(r"scale\(([-\d.]+)\)", transform)
        tx, ty = (float(translate.group(1)), float(translate.group(2))) if translate else (0.0, 0.0)
        sc = float(scale.group(1)) if scale else 1.0
        points += [(tx + x * sc, ty + y * sc) for x, y in raw_points(inner)]
    rest = re.sub(r'<g transform="[^"]+">.*?</g>', "", shapes, flags=re.S)
    return points + raw_points(rest)


def main() -> None:
    source = SRC.read_text(encoding="utf-8")
    body = source[source.index("export const PREFECTURES") :]
    body = body[body.index("= [") + 2 :]
    prefectures = json.loads(body[: body.rindex("]") + 1])

    lines = [
        "// 自動生成: scripts/gen_centroids.py（japanPaths.ts の各県 bbox 中心を viewBox 座標へ換算）",
        '// viewBox = "0 0 1000 1000"。OUTER/INNER トランスフォーム適用後の座標。',
        "export const PREF_CENTROIDS: Record<number, { x: number; y: number }> = {",
    ]
    for pref in sorted(prefectures, key=lambda p: p["code"]):
        points = shape_points(pref["shapes"])
        xs = [x for x, _ in points]
        ys = [y for _, y in points]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        if pref["code"] == 47:
            tx, ty, sc = OKINAWA_INSET
        else:
            translate = re.search(r"translate\(([-\d.]+)[ ,]+([-\d.]+)\)", pref["transform"])
            tx, ty, sc = float(translate.group(1)), float(translate.group(2)), 1.0
        x = OUTER_SCALE * (tx + cx * sc + INNER_OFFSET[0]) + OUTER_OFFSET[0]
        y = OUTER_SCALE * (ty + cy * sc + INNER_OFFSET[1]) + OUTER_OFFSET[1]
        lines.append(f"  {pref['code']}: {{ x: {x:.1f}, y: {y:.1f} }}, // {pref['name']}")
    lines.append("};")
    DEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {DEST} ({len(prefectures)} prefectures)")


if __name__ == "__main__":
    main()
