"""Normalize human-provided imagegen PNGs for the quiz renderer."""

from __future__ import annotations

from PIL import Image, ImageOps

from common import WORK


TARGET_SIZE = (1536, 1024)
TARGET_ASPECT = TARGET_SIZE[0] / TARGET_SIZE[1]
# 3:2 ちょうどでなくてもこの範囲なら切り捨ては 1% 未満で実害がない
ASPECT_TOLERANCE = 0.01


def main() -> None:
    """Center-crop raw PNGs to 3:2 and save renderer-ready RGB PNGs."""
    source = WORK / "illustrations_raw"
    destination = WORK / "illustrations"
    destination.mkdir(parents=True, exist_ok=True)
    inputs = sorted(source.glob("*.png"))
    if not inputs:
        raise RuntimeError(f"No PNG files found in {source}")
    cropped: list[tuple[str, float]] = []
    for path in inputs:
        with Image.open(path) as image:
            aspect = image.width / image.height
            if abs(aspect - TARGET_ASPECT) > ASPECT_TOLERANCE:
                loss = 1 - min(TARGET_ASPECT / aspect, aspect / TARGET_ASPECT)
                cropped.append((path.name, loss * 100))
            normalized = ImageOps.fit(
                image.convert("RGB"),
                TARGET_SIZE,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            normalized.save(destination / path.name, format="PNG")
    print(f"normalized {len(inputs)} illustrations to {destination}")
    if cropped:
        # 3:2 で生成されなかった素材はここで端が捨てられる。被写体が欠けた場合は
        # サイズを明示して再生成する（プロンプトの SIZE_LINE = export_prompts.py）
        print(f"WARNING: {len(cropped)} illustrations were not 3:2 and got cropped")
        for name, loss in sorted(cropped, key=lambda item: -item[1]):
            print(f"  {name}: 幅の {loss:.1f}% を切り捨て")


if __name__ == "__main__":
    main()
