"""imagegen で生成した背景を原本 PNG と描画用 JPEG へ正規化する。"""

from __future__ import annotations

import argparse

from common import REMOTION_DIR, WORK


TARGET_SIZE = (1080, 1920)
TARGET_ASPECT = TARGET_SIZE[0] / TARGET_SIZE[1]
# この範囲なら中央クロップによる切り捨てが 1% 未満で実害がない。
ASPECT_TOLERANCE = 0.01
JPEG_QUALITY = 88


def main(argv: list[str] | None = None) -> int:
    """raw 背景を中央クロップし、用途別の 2 形式へ保存する。"""
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    # ホストには PIL を入れない運用のため、--help の解析後に Docker 内でだけ読む。
    from PIL import Image, ImageOps

    source = WORK / "backgrounds_raw"
    png_destination = WORK / "backgrounds"
    jpeg_destination = REMOTION_DIR / "public" / "bg"
    png_destination.mkdir(parents=True, exist_ok=True)
    jpeg_destination.mkdir(parents=True, exist_ok=True)
    inputs = sorted(
        (*source.glob("*.png"), *source.glob("*.jpg"), *source.glob("*.jpeg"))
    )
    if not inputs:
        raise RuntimeError(f"PNG/JPG ファイルがありません: {source}")
    stems = [path.stem for path in inputs]
    duplicates = sorted({stem for stem in stems if stems.count(stem) > 1})
    if duplicates:
        raise RuntimeError(f"同じ content_key の画像が複数あります: {', '.join(duplicates)}")
    cropped: list[tuple[str, float]] = []
    for path in inputs:
        with Image.open(path) as image:
            aspect = image.width / image.height
            if abs(aspect - TARGET_ASPECT) > ASPECT_TOLERANCE:
                loss = 1 - min(TARGET_ASPECT / aspect, aspect / TARGET_ASPECT)
                cropped.append((path.name, loss * 100))
            normalized = ImageOps.fit(
                image.convert("RGB"), TARGET_SIZE,
                method=Image.Resampling.LANCZOS, centering=(0.5, 0.5),
            )
            normalized.save(png_destination / f"{path.stem}.png", format="PNG")
            # 大きな PNG は Remotion の delayRender をタイムアウトさせるため JPEG にする。
            normalized.save(
                jpeg_destination / f"{path.stem}.jpg", format="JPEG",
                quality=JPEG_QUALITY, optimize=True,
            )
    print(f"{len(inputs)} 件の背景を正規化しました")
    if cropped:
        print(f"WARNING: {len(cropped)} 件は 9:16 でないため中央クロップしました")
        for name, loss in sorted(cropped, key=lambda item: -item[1]):
            print(f"  {name}: 画像領域の {loss:.1f}% を切り捨て")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
