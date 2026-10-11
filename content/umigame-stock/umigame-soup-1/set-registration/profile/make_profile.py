"""探偵カメロックのプロフィール画像（1080×1080）を立ち絵から作る（21-7a2）.

立ち絵（透過 PNG）を正方形に切り抜いて単色の背景に重ねる。文字は入れない。
候補ごとの元画像・切り抜き範囲・背景色は CANDIDATES に持つ。

使い方（リポジトリルートから）:
    python3 content/umigame-stock/umigame-soup-1/set-registration/profile/make_profile.py
        → candidates/ に全候補と円形マスクの見え方（1080 / 320 / 110px）を出力
    python3 .../make_profile.py --pick B
        → 候補 B を profile.png として確定出力
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CHAR_DIR = REPO / "content/video-build/umigame-soup-1/assets/characters"
SIZE = 1080
# 円の内側 7 割（半径比 0.7）に顔の矩形の四隅が収まることを検査する。
FACE_LIMIT = 0.7
# 顔（帽子を除く目・頬・口）の矩形。元画像上の (左, 上, 右, 下)。目視で測った値。
FACE_BOX = {
    "master_base.png": (450, 190, 700, 370),
    "master_happy.png": (440, 175, 680, 370),
}

# 切り抜きは元画像（1000×1100）上の正方形: (中心 x, 中心 y, 一辺)。
# 背景色は動画（remotion/）で使っている色から選ぶ。
CANDIDATES: dict[str, dict] = {
    "A": {
        "label": "顔のアップ・ネイビー",
        "source": "master_base.png",
        "crop": (550, 280, 520),
        "bg": "#16232b",
    },
    "B": {
        "label": "上半身（笑顔・スープを掲げる）・ゴールド",
        "source": "master_happy.png",
        "crop": (545, 345, 780),
        "bg": "#ffc42e",
    },
    "C": {
        "label": "上半身（虫眼鏡とスープ）・ライトブルー",
        "source": "master_base.png",
        "crop": (590, 365, 780),
        "bg": "#e8f5ff",
    },
}


def render(key: str) -> Image.Image:
    """候補を 1080×1080 の RGB 画像として描く.

    Args:
        key: CANDIDATES のキー。

    Returns:
        背景色に立ち絵を重ねた正方形画像。
    """
    spec = CANDIDATES[key]
    src = Image.open(CHAR_DIR / spec["source"]).convert("RGBA")
    cx, cy, side = spec["crop"]
    half = side // 2
    box = (cx - half, cy - half, cx - half + side, cy - half + side)
    # 元画像の外側は透明として扱う（crop は範囲外を透明で埋める）。
    cut = src.crop(box).resize((SIZE, SIZE), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), spec["bg"])
    canvas.alpha_composite(cut)
    return canvas.convert("RGB")


def face_ratio(key: str) -> float:
    """顔の矩形の四隅のうち中心から最も遠い点の距離を、円の半径比で返す.

    Args:
        key: CANDIDATES のキー。

    Returns:
        最遠点の距離 / (1080 / 2)。FACE_LIMIT 以下なら円の内側 7 割に収まる。
    """
    spec = CANDIDATES[key]
    cx, cy, side = spec["crop"]
    scale = SIZE / side
    left, top, right, bottom = FACE_BOX[spec["source"]]
    far = max(
        ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        for x in (left, right)
        for y in (top, bottom)
    )
    return far * scale / (SIZE / 2)


def circle_preview(img: Image.Image, size: int) -> Image.Image:
    """Instagram の円形表示を模した見え方を作る（外側は白）.

    Args:
        img: 1080×1080 の候補画像。
        size: 表示サイズ（px）。

    Returns:
        円形マスクをかけて縮小した画像。
    """
    scale = 4
    mask = Image.new("L", (size * scale, size * scale), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * scale - 1, size * scale - 1), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    small = img.resize((size, size), Image.LANCZOS)
    out = Image.new("RGB", (size, size), "#ffffff")
    out.paste(small, (0, 0), mask)
    return out


def main() -> None:
    """候補一式、または確定版の profile.png を出力する."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--pick", choices=sorted(CANDIDATES), help="確定する候補")
    args = parser.parse_args()

    if args.pick:
        assert face_ratio(args.pick) <= FACE_LIMIT
        render(args.pick).save(HERE / "profile.png")
        print(f"profile.png <- {args.pick}: {CANDIDATES[args.pick]['label']}")
        return

    out_dir = HERE / "candidates"
    out_dir.mkdir(exist_ok=True)
    for key, spec in CANDIDATES.items():
        img = render(key)
        ratio = face_ratio(key)
        assert ratio <= FACE_LIMIT, f"{key}: 顔が円の内側 7 割を出る ({ratio:.2f})"
        img.save(out_dir / f"{key}.png")
        for size in (1080, 320, 110):
            circle_preview(img, size).save(out_dir / f"{key}_circle_{size}.png")
        print(f"{key}: {spec['label']}（顔の最遠点 = 半径の {ratio:.2f}）")


if __name__ == "__main__":
    main()
