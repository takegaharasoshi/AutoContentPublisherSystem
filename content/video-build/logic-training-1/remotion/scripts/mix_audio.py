"""レンダリング済み映像への音声ミックスとレビュー用スチルの書き出し。

image-batch イメージ（ffmpeg 入り）の中で実行する。BGM の LRU 選曲と SE の
固定ディレイ（tick 8.0 秒 / chime 13.0 秒）は R-1 の不変条件のため、
フィルタは ``gpt_quiz_multicut._build_video`` の最終パスと同値にしてある。
BGM は台帳（work/build_manifest.json）に記録済みの音源をそのまま使い、
LRU（``audio_assets.last_used_at``）の更新は呼び出し側が担う。
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import tempfile

import boto3

from spec import (
    BGM_FADE_OUT_DURATION,
    BGM_FADE_OUT_START,
    BGM_VOLUME,
    CHIME_GAIN_DB,
    CHIME_SECONDS,
    DURATION_SECONDS,
    STILL_FRAMES,
    TICK_GAIN_DB,
    TICK_SECONDS,
)

SET_CODE = "logic-training-1"
TICK_VOLUME = 10 ** (TICK_GAIN_DB / 20)
CHIME_VOLUME = 10 ** (CHIME_GAIN_DB / 20)
TICK_DELAY_MILLISECONDS = int(TICK_SECONDS * 1_000)
CHIME_DELAY_MILLISECONDS = int(CHIME_SECONDS * 1_000)


def _download(client, bucket: str, key: str, path: Path) -> None:
    """Fetch one audio object into the temporary working directory."""
    path.write_bytes(client.get_object(Bucket=bucket, Key=key)["Body"].read())


def main() -> None:
    """Mux BGM and the two sound effects onto the silent Remotion output."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--bgm-key", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--stills-dir")
    args = parser.parse_args()

    bucket = os.environ.get("S3_BUCKET_NAME")
    if not bucket:
        raise RuntimeError("S3_BUCKET_NAME is required")
    client = boto3.client("s3")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        bgm, tick, chime = temp / "bgm.m4a", temp / "tick.m4a", temp / "chime.m4a"
        _download(client, bucket, args.bgm_key, bgm)
        _download(client, bucket, f"audio/{SET_CODE}/se/countdown_tick.m4a", tick)
        _download(client, bucket, f"audio/{SET_CODE}/se/answer_chime.m4a", chime)

        filters = [
            f"[1:a]volume={BGM_VOLUME:.6f},"
            f"atrim=0:{DURATION_SECONDS},"
            f"afade=t=out:st={BGM_FADE_OUT_START}:"
            f"d={BGM_FADE_OUT_DURATION},asetpts=PTS-STARTPTS[bgm]",
            f"[2:a]volume={TICK_VOLUME:.6f},"
            f"adelay={TICK_DELAY_MILLISECONDS}|{TICK_DELAY_MILLISECONDS}[tick]",
            f"[3:a]volume={CHIME_VOLUME:.6f},"
            f"adelay={CHIME_DELAY_MILLISECONDS}|{CHIME_DELAY_MILLISECONDS}[chime]",
            f"[bgm][tick][chime]amix=inputs=3:duration=longest:"
            f"normalize=0,atrim=0:{DURATION_SECONDS}[a]",
        ]
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        command = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", args.video,
            "-stream_loop", "-1", "-i", str(bgm),
            "-i", str(tick),
            "-i", str(chime),
            "-filter_complex", ";".join(filters),
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-movflags", "+faststart",
            "-c:a", "aac", "-t", str(DURATION_SECONDS),
            str(output),
        ]
        subprocess.run(command, check=True)
        print(f"mixed: {output}")

        if args.stills_dir:
            stills_dir = Path(args.stills_dir)
            stills_dir.mkdir(parents=True, exist_ok=True)
            for key, frame in STILL_FRAMES.items():
                still = stills_dir / f"{output.stem}_{key}.png"
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-loglevel", "error",
                        "-i", str(output),
                        "-vf", f"select=eq(n\\,{frame})",
                        "-vsync", "0", "-frames:v", "1", str(still),
                    ],
                    check=True,
                )
                print(f"still: {still}")


if __name__ == "__main__":
    main()
