"""コーチ立ち絵を S3 から取得し、Remotion の public/ へ配置する。

image-batch イメージ（boto3 + Pillow 入り）の中で実行する。4 表情は共通の
キャンバス（下端中央そろえ）で作られているため、**4 枚の不透明領域の和**で
同じ矩形を切り出す（現行レンダラー ``_trim_coaches`` と同じ扱い）。カット間で
相対サイズ・立ち位置が動かないようにするための処理で、1 枚ずつ trim しては
いけない。
"""

from __future__ import annotations

from io import BytesIO
import os
from pathlib import Path

import boto3
from PIL import Image

SET_CODE = "logic-training-1"
COACH_FILENAMES = {
    "hook": "coach_hook.png",
    "question": "coach_question.png",
    "think": "coach_think.png",
    "answer": "coach_answer.png",
}
PUBLIC = Path(__file__).resolve().parents[1] / "public"


def main() -> None:
    """Download, jointly trim and store the four coach poses."""
    bucket = os.environ.get("S3_BUCKET_NAME")
    if not bucket:
        raise RuntimeError("S3_BUCKET_NAME is required")
    client = boto3.client("s3")
    images: dict[str, Image.Image] = {}
    for pose, filename in COACH_FILENAMES.items():
        key = f"assets/{SET_CODE}/{filename}"
        body = client.get_object(Bucket=bucket, Key=key)["Body"].read()
        with Image.open(BytesIO(body)) as image:
            image.load()
            images[pose] = image.convert("RGBA")

    boxes = [image.getbbox() for image in images.values()]
    if all(box is not None for box in boxes):
        left = min(box[0] for box in boxes)
        top = min(box[1] for box in boxes)
        right = max(box[2] for box in boxes)
        bottom = max(box[3] for box in boxes)
        images = {
            pose: image.crop((left, top, right, bottom))
            for pose, image in images.items()
        }

    destination = PUBLIC / "coach"
    destination.mkdir(parents=True, exist_ok=True)
    for pose, image in images.items():
        path = destination / COACH_FILENAMES[pose]
        image.save(path, format="PNG")
        print(f"{path.name}: {image.width}x{image.height}")


if __name__ == "__main__":
    main()
