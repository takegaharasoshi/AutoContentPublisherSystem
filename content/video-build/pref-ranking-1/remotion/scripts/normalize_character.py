"""表彰台五郎のポーズ 3 種を共通キャンバス・共通倍率へ正規化する（17-4b）。

生成 AI で作ったポーズ画像は 1 枚ごとにキャラの寸法・立ち位置が微妙に違うため、
そのまま差し替えるとポーズが変わるたびにキャラが伸縮・跳躍して見える。
logic-training-1 の 15-13（コーチ 4 表情）と同じ手法で、**共通倍率で拡縮 →
共通キャンバスへ下端そろえ**して正式アセットにする。

五郎は「3 段表彰台がボディ」のキャラで、腕・軍配・瓢箪はポーズごとに大きく動くため、
不透明画素の外接矩形は基準にならない。本スクリプトは**ボディ前面の「1」の字**
（黒の連結成分のうち、外郭線を除いた最大のもの）を基準に倍率と左右位置を決め、
**足元（不透明画素の下端）**で上下をそろえる。

Pillow が要るためリポジトリの慣例どおり Docker 経由で実行する:

    docker run --rm -u $(id -u):$(id -g) -v "$PWD:/work" -w /work \\
      --entrypoint python image-batch:ffmpeg-check scripts/normalize_character.py \\
      --source work/char-src --dest public/char
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image

# 出力の共通キャンバス（S3 の固定アセット。レンダラーは幅だけ指定して使う）
CANVAS = (1160, 1220)
# 「1」の字の高さをこの値へそろえる（= 共通倍率の基準）
GLYPH_TARGET_HEIGHT = 156.0
# キャンバス下端から足元までの余白（バウンドのアニメーション分を残す）
FOOT_MARGIN = 40

# 出力名 → 元ポーズのファイル名（S3 assets/pref-ranking-1/source/ に置いてある）
POSES = {
    "goro_base": "goro_base_raw.png",
    "goro_suspense": "goro_suspense_raw.png",
    "goro_gunbai": "goro_gunbai_raw.png",
}


def alpha_bottom(image: Image.Image) -> int:
    """Return the lowest row that still holds a visible pixel."""
    bbox = image.getchannel("A").point(lambda v: 255 if v > 32 else 0).getbbox()
    if bbox is None:
        raise RuntimeError("透過画素しかない画像")
    return bbox[3]


def body_glyph(image: Image.Image) -> tuple[int, int, int, int]:
    """Locate the black "1" drawn on the podium body.

    The outline of the whole character is also black and forms the largest dark
    component, so the glyph is taken as the largest *inner* component.

    Args:
        image: RGBA source image.

    Returns:
        (x_min, x_max, y_min, y_max) of the glyph in source pixels.
    """
    width, height = image.size
    pixels = image.load()
    dark = [
        [1 if (pixels[x, y][3] > 128 and max(pixels[x, y][:3]) < 80) else 0 for x in range(width)]
        for y in range(height)
    ]
    seen = [[0] * width for _ in range(height)]
    components: list[tuple[int, int, int, int, int]] = []
    for y in range(height):
        for x in range(width):
            if not dark[y][x] or seen[y][x]:
                continue
            queue = deque([(x, y)])
            seen[y][x] = 1
            points = []
            while queue:
                cx, cy = queue.popleft()
                points.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height and dark[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = 1
                        queue.append((nx, ny))
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            components.append((len(points), min(xs), max(xs), min(ys), max(ys)))
    components.sort(reverse=True)
    # 最大 = 外郭線。以降から「縦長（h > w）で最大」のものを「1」とみなす
    for _, x_min, x_max, y_min, y_max in components[1:]:
        if (y_max - y_min) > (x_max - x_min):
            return x_min, x_max, y_min, y_max
    raise RuntimeError("ボディの「1」を特定できなかった")


def normalize(source: Path, dest: Path) -> None:
    """Scale and align every pose onto the shared canvas.

    Args:
        source: Directory holding the raw pose PNGs.
        dest: Directory to write the normalized PNGs into.
    """
    dest.mkdir(parents=True, exist_ok=True)
    for name, filename in POSES.items():
        image = Image.open(source / filename).convert("RGBA")
        x_min, x_max, y_min, y_max = body_glyph(image)
        scale = GLYPH_TARGET_HEIGHT / (y_max - y_min)
        glyph_center_x = (x_min + x_max) / 2
        feet = alpha_bottom(image)

        resized = image.resize(
            (round(image.width * scale), round(image.height * scale)), Image.LANCZOS
        )
        canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        offset_x = round(CANVAS[0] / 2 - glyph_center_x * scale)
        offset_y = round(CANVAS[1] - FOOT_MARGIN - feet * scale)
        canvas.alpha_composite(resized, (offset_x, offset_y))
        bbox = canvas.getchannel("A").point(lambda v: 255 if v > 32 else 0).getbbox()
        if bbox is None or bbox[0] < 0 or bbox[1] < 0 or bbox[2] > CANVAS[0] or bbox[3] > CANVAS[1]:
            raise RuntimeError(f"{name}: キャンバスに収まっていない ({bbox})")
        canvas.save(dest / f"{name}.png")
        print(
            f"{name}.png  倍率 {scale:.3f}  中身 x {bbox[0]}..{bbox[2]} y {bbox[1]}..{bbox[3]}"
        )


def main() -> None:
    """Run the normalization."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="試作ポーズ PNG の置き場")
    parser.add_argument("--dest", type=Path, required=True, help="正規化後の出力先")
    args = parser.parse_args()
    normalize(args.source, args.dest)


if __name__ == "__main__":
    main()
