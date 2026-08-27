"""pref-ranking-1 の Instagram プロフィール画像（アイコン）を生成する。

採用案は "cream"（生成り地 + 淡墨茶リング。2026-08-27 ユーザー判断）で、
既定でこの案を profile_icon.png として出力する。--variant で不採用案
（dark / gunbai）も再現でき、--compare で円クロップ + 実表示サイズの
比較シートを work/ に出す。

設計上の制約:
  - 色は remotion/src/theme.ts のパレットに合わせる（生成り・淡墨茶・金・朱）
  - Instagram は円クロップで表示するため、顔・鉢巻・胴体の「1」を内接円の
    内側に収める。脚は落としたバスト構図にし、断ち切りが表彰台の胴体に来る
    ようにする（細い脚の途中で切れると欠損に見えるため）
  - 文字は入れない（40px 表示で潰れる。ワードは Instagram の名前欄が担う）
  - 軍配ポーズは「1 位発表時のみ」というキャラ制約（セット別設計書 セクション 8）が
    あるため常設のアイコンには使わない

入力は remotion/public/char/*.png（S3 の正式キャラクターアセット。git 管理外で、
README の事前準備で配置する）。PIL が要るためホストではなくコンテナで実行する:

    docker run --rm -v "$PWD:/work" -w /work --user "$(id -u)" \
      --entrypoint python image-batch:ffmpeg-check \
      content/video-build/pref-ranking-1/account/build_profile_icon.py
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = Path(__file__).resolve().parent
CHAR_DIR = BASE_DIR.parent / "remotion" / "public" / "char"
WORK_DIR = BASE_DIR.parent / "work" / "profile"

SIZE = 1080  # Instagram の推奨（正方形。表示時に円クロップされる）
SS = 2  # スーパーサンプリング倍率

# theme.ts のパレット
CREAM = (246, 240, 225, 255)
CREAM_DEEP = (239, 228, 204, 255)
SUMI_DEEP = (84, 74, 60, 255)
SUMI_BASE = (99, 89, 74, 255)
GOLD = (217, 166, 46, 255)
GOLD_DEEP = (192, 134, 24, 255)
GOLD_LIGHT = (244, 215, 125, 255)

# 元画像（1160x1220 の正規化済みキャラクター）での切り出し・基準矩形
BASE_CROP = (60, 250, 1120, 972)  # 脚を落とすバスト切り出し（台座の下端で切る）
BASE_FOCUS = (230, 300, 1010, 972)  # マイク〜指先 / 鉢巻の上〜台座の下
GUNBAI_CROP = (200, 40, 1160, 1000)
GUNBAI_FOCUS = (240, 60, 1150, 1000)


def radial_bg(size: int, inner: tuple, outer: tuple) -> Image.Image:
    """中心 inner → 外周 outer の放射グラデーション背景を作る。

    Args:
        size: 一辺のピクセル数。
        inner: 中心色（RGBA）。
        outer: 外周色（RGBA）。

    Returns:
        グラデーション画像。
    """
    img = Image.new("RGBA", (size, size))
    px = img.load()
    center = (size - 1) / 2
    max_r = math.hypot(center, center)
    for y in range(size):
        for x in range(size):
            t = min(1.0, math.hypot(x - center, y - center) / max_r) ** 1.15
            px[x, y] = tuple(int(inner[i] + (outer[i] - inner[i]) * t) for i in range(4))
    return img


def sunburst(size: int, color: tuple, rays: int, alpha: int) -> Image.Image:
    """中心から放射する光条レイヤー（お祭り感の演出）を作る。

    Args:
        size: 一辺のピクセル数。
        color: 光条の色（RGBA。alpha は引数の alpha で上書きする）。
        rays: 光条の本数。
        alpha: 光条の不透明度（0-255）。

    Returns:
        透明背景の光条レイヤー。
    """
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    center = size / 2
    half = math.pi / rays * 0.44
    for i in range(rays):
        a = 2 * math.pi * i / rays + math.pi / rays / 2
        draw.polygon(
            [
                (center, center),
                (center + size * math.cos(a - half), center + size * math.sin(a - half)),
                (center + size * math.cos(a + half), center + size * math.sin(a + half)),
            ],
            fill=color[:3] + (alpha,),
        )
    return layer.filter(ImageFilter.GaussianBlur(size / 240))


def draw_ring(canvas: Image.Image, outer: tuple, inner: tuple, width_ratio: float) -> None:
    """外周のリング（太い環 + 内側の細いヘアライン）を描く。

    Args:
        canvas: 描画先。
        outer: 太い環の色（RGBA）。
        inner: ヘアラインの色（RGBA）。
        width_ratio: 太い環の幅（一辺に対する比）。
    """
    size = canvas.size[0]
    draw = ImageDraw.Draw(canvas)
    width = size * width_ratio
    inset = size * 0.017
    draw.ellipse([inset, inset, size - inset, size - inset], outline=outer, width=int(width))
    inset2 = inset + width * 1.8
    draw.ellipse(
        [inset2, inset2, size - inset2, size - inset2],
        outline=inner,
        width=max(2, int(size * 0.005)),
    )


def place_char(
    canvas: Image.Image,
    name: str,
    crop: tuple,
    focus: tuple,
    center_x: float,
    bottom: float,
    focus_w: float,
) -> None:
    """キャラクターを切り出し・拡縮して配置する。

    Args:
        canvas: 描画先。
        name: remotion/public/char 配下のファイル名（拡張子なし）。
        crop: 元画像から切り出す矩形。
        focus: 基準矩形（元画像座標）。この幅が focus_w になるよう拡縮する。
        center_x: focus の水平中心を置く canvas 座標。
        bottom: focus の下端を置く canvas 座標。
        focus_w: focus の目標幅。
    """
    char = Image.open(CHAR_DIR / f"{name}.png").convert("RGBA").crop(crop)
    fx0, fy0, fx1, fy1 = (focus[0] - crop[0], focus[1] - crop[1],
                          focus[2] - crop[0], focus[3] - crop[1])
    scale = focus_w / (fx1 - fx0)
    char = char.resize((int(char.width * scale), int(char.height * scale)), Image.LANCZOS)
    left = int(center_x - (fx0 + fx1) / 2 * scale)
    top = int(bottom - fy1 * scale)

    blur = canvas.size[0] / 90
    shadow_src = Image.new("RGBA", char.size, (60, 50, 38, 255))
    shadow_src.putalpha(char.split()[3].point(lambda v: int(v * 0.32)))
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    blurred = shadow_src.filter(ImageFilter.GaussianBlur(blur))
    shadow.paste(blurred, (left, int(top + blur)), blurred)
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(char, (left, top))


def build(variant: str) -> Image.Image:
    """指定案のアイコンを生成する。

    Args:
        variant: "cream"（採用）/ "dark" / "gunbai"。

    Returns:
        SIZE 四方の RGBA 画像。

    Raises:
        ValueError: 未知の variant を指定した場合。
    """
    size = SIZE * SS
    if variant == "cream":
        canvas = radial_bg(size, CREAM, CREAM_DEEP)
        canvas.alpha_composite(sunburst(size, GOLD_DEEP, 24, 20))
        draw_ring(canvas, SUMI_DEEP, GOLD[:3] + (200,), 0.024)
        place_char(canvas, "goro_base", BASE_CROP, BASE_FOCUS,
                   size * 0.5, size * 1.01, size * 0.80)
    elif variant == "dark":
        canvas = radial_bg(size, SUMI_BASE, SUMI_DEEP)
        canvas.alpha_composite(sunburst(size, GOLD_LIGHT, 24, 26))
        draw_ring(canvas, GOLD, GOLD_LIGHT[:3] + (150,), 0.021)
        place_char(canvas, "goro_base", BASE_CROP, BASE_FOCUS,
                   size * 0.5, size * 1.01, size * 0.80)
    elif variant == "gunbai":
        canvas = radial_bg(size, SUMI_BASE, SUMI_DEEP)
        canvas.alpha_composite(sunburst(size, GOLD_LIGHT, 24, 26))
        draw_ring(canvas, GOLD, GOLD_LIGHT[:3] + (150,), 0.021)
        place_char(canvas, "goro_gunbai", GUNBAI_CROP, GUNBAI_FOCUS,
                   size * 0.47, size * 1.01, size * 0.86)
    else:
        raise ValueError(f"unknown variant: {variant}")
    return canvas.resize((SIZE, SIZE), Image.LANCZOS)


def circle_preview(img: Image.Image, px: int) -> Image.Image:
    """円クロップした縮小プレビューを作る（小サイズでの視認性確認用）。

    Args:
        img: 元画像。
        px: プレビューの一辺。

    Returns:
        白地に円クロップした画像。
    """
    small = img.resize((px, px), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (px * 4, px * 4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, px * 4 - 1, px * 4 - 1], fill=255)
    out = Image.new("RGBA", (px, px), (255, 255, 255, 255))
    out.paste(small, (0, 0), mask.resize((px, px), Image.LANCZOS))
    return out


def main() -> None:
    """コマンドライン実行のエントリポイント。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", default="cream", choices=["cream", "dark", "gunbai"])
    parser.add_argument("--compare", action="store_true",
                        help="3 案の比較シートを work/profile/ に出力する")
    args = parser.parse_args()

    if args.compare:
        WORK_DIR.mkdir(parents=True, exist_ok=True)
        variants = ["cream", "dark", "gunbai"]
        images = {v: build(v) for v in variants}
        cell = 360
        sheet = Image.new("RGBA", (cell * len(variants) + 40, 560), (250, 250, 250, 255))
        for i, v in enumerate(variants):
            x = 20 + i * cell
            for px, pos in ((320, (x, 20)), (110, (x, 370)), (40, (x + 140, 370))):
                preview = circle_preview(images[v], px)
                sheet.paste(preview, pos, preview)
            ImageDraw.Draw(sheet).text((x, 500), v, fill=(40, 40, 40))
        for v, img in images.items():
            img.convert("RGB").save(WORK_DIR / f"profile_{v}.png")
        sheet.convert("RGB").save(WORK_DIR / "compare.png")
        print(f"wrote {WORK_DIR}")
        return

    out = BASE_DIR / "profile_icon.png"
    build(args.variant).convert("RGB").save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
