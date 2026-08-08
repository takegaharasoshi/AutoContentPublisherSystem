"""Normalize human-provided imagegen PNGs for the quiz renderer."""

from __future__ import annotations

from PIL import Image, ImageOps

from common import WORK


TARGET_SIZE = (1536, 1024)


def main() -> None:
    """Center-crop raw PNGs to 3:2 and save renderer-ready RGB PNGs."""
    source = WORK / "illustrations_raw"
    destination = WORK / "illustrations"
    destination.mkdir(parents=True, exist_ok=True)
    inputs = sorted(source.glob("*.png"))
    if not inputs:
        raise RuntimeError(f"No PNG files found in {source}")
    for path in inputs:
        with Image.open(path) as image:
            normalized = ImageOps.fit(
                image.convert("RGB"),
                TARGET_SIZE,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            normalized.save(destination / path.name, format="PNG")
    print(f"normalized {len(inputs)} illustrations to {destination}")


if __name__ == "__main__":
    main()
