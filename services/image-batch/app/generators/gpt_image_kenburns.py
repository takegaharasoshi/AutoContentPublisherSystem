"""GPT Image plus Ken Burns video generator."""

from __future__ import annotations

import logging
from io import BytesIO
from pathlib import Path
import subprocess
import tempfile
from typing import Any

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from acps_shared.s3 import get_object

from ..clock import now_utc
from . import openai_image
from .contracts import (
    GeneratorContext,
    GeneratorResult,
    IntermediateOutput,
    MediaOutput,
)


logger = logging.getLogger(__name__)

FFMPEG_BINARY = "ffmpeg"
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
OUTPUT_FPS = 30
OUTPUT_DURATION_SECONDS = 10
OUTPUT_CRF = 20
FFMPEG_TIMEOUT_SECONDS = 600
ZOOM_START = 1.0
ZOOM_END = 1.08
SUPERSAMPLE_FACTOR = 2
BACKGROUND_BLUR_RADIUS = 48
BACKGROUND_BRIGHTNESS = 0.72
BACKGROUND_BLUR_DOWNSCALE = 4
CANVAS_JPEG_QUALITY = 90
SAFE_BOX_MARGIN = 8


def _compose_canvas(jpeg: bytes) -> bytes:
    """Place the full source image over a blurred vertical background."""
    # zoompan は終端 ZOOM_END 倍まで中央にズームするため、常時可視な領域は
    # 出力寸法を ZOOM_END で割ったサイズになる。zoompan が整数ピクセルで
    # 丸める分を SAFE_BOX_MARGIN で吸収し、前景が端で削れないようにする。
    safe_box = (
        int(OUTPUT_WIDTH / ZOOM_END) - SAFE_BOX_MARGIN,
        int(OUTPUT_HEIGHT / ZOOM_END) - SAFE_BOX_MARGIN,
    )
    background_size = (OUTPUT_WIDTH, OUTPUT_HEIGHT)
    downscaled_size = (
        OUTPUT_WIDTH // BACKGROUND_BLUR_DOWNSCALE,
        OUTPUT_HEIGHT // BACKGROUND_BLUR_DOWNSCALE,
    )
    with Image.open(BytesIO(jpeg)) as image:
        source = image.convert("RGB")
        foreground = ImageOps.contain(source, safe_box, Image.LANCZOS)
        background = ImageOps.fit(source, background_size, Image.LANCZOS)
        downscaled_background = background.resize(
            downscaled_size, Image.LANCZOS
        )
        blurred_background = downscaled_background.filter(
            ImageFilter.GaussianBlur(
                BACKGROUND_BLUR_RADIUS / BACKGROUND_BLUR_DOWNSCALE
            )
        )
        expanded_background = blurred_background.resize(
            background_size, Image.LANCZOS
        )
        canvas = ImageEnhance.Brightness(expanded_background).enhance(
            BACKGROUND_BRIGHTNESS
        )
        offset = (
            (OUTPUT_WIDTH - foreground.width) // 2,
            (OUTPUT_HEIGHT - foreground.height) // 2,
        )
        canvas.paste(foreground, offset)
        output = BytesIO()
        canvas.save(output, format="JPEG", quality=CANVAS_JPEG_QUALITY)
    return output.getvalue()


def _build_zoompan_filter() -> str:
    """Build the Ken Burns filter from output and zoom constants."""
    total_frames = OUTPUT_FPS * OUTPUT_DURATION_SECONDS
    zoom_denominator = total_frames - 1
    zoom_delta = ZOOM_END - ZOOM_START
    supersample_width = OUTPUT_WIDTH * SUPERSAMPLE_FACTOR
    supersample_height = OUTPUT_HEIGHT * SUPERSAMPLE_FACTOR
    return (
        f"[0:v]scale={supersample_width}:{supersample_height},"
        f"zoompan=z='{ZOOM_START:.1f}+{zoom_delta:.2f}*on/"
        f"{zoom_denominator}':x='iw/2-(iw/zoom/2)':"
        f"y='ih/2-(ih/zoom/2)':d=1:"
        f"s={OUTPUT_WIDTH}x{OUTPUT_HEIGHT}:fps={OUTPUT_FPS},"
        "format=yuv420p[v]"
    )


def _select_audio_asset(cursor: Any, set_id: int) -> tuple[int, str]:
    """Select the least-recently-used active audio asset."""
    cursor.execute(
        "SELECT id, s3_key FROM audio_assets "
        "WHERE set_id = %s AND asset_type = 'bgm' AND is_active = 1 "
        "ORDER BY last_used_at ASC, id ASC LIMIT 1",
        (set_id,),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError(f"No active audio_assets for set_id={set_id}")
    return int(row[0]), str(row[1])


def _build_video(jpeg: bytes, audio: bytes) -> bytes:
    """Encode one JPEG and preprocessed AAC audio as an MP4."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        source_path = temp_path / "source.jpg"
        audio_path = temp_path / "audio.m4a"
        output_path = temp_path / "out.mp4"
        source_path.write_bytes(jpeg)
        audio_path.write_bytes(audio)
        command = [
            FFMPEG_BINARY,
            "-y",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-framerate",
            str(OUTPUT_FPS),
            "-t",
            str(OUTPUT_DURATION_SECONDS),
            "-i",
            str(source_path),
            "-i",
            str(audio_path),
            "-filter_complex",
            _build_zoompan_filter(),
            "-map",
            "[v]",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-crf",
            str(OUTPUT_CRF),
            "-preset",
            "medium",
            "-movflags",
            "+faststart",
            "-c:a",
            "copy",
            "-shortest",
            "-t",
            str(OUTPUT_DURATION_SECONDS),
            str(output_path),
        ]
        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                timeout=FFMPEG_TIMEOUT_SECONDS,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            stderr = exc.stderr or b""
            if isinstance(stderr, bytes):
                stderr_text = stderr.decode(errors="replace")
            else:
                stderr_text = stderr
            logger.error("ffmpeg failed: %s", stderr_text[-500:])
            raise

        video = output_path.read_bytes()
        if not video:
            raise RuntimeError("ffmpeg produced an empty output file")
        return video


def generate(context: GeneratorContext) -> GeneratorResult:
    """Generate a ten-second vertical Ken Burns MP4."""
    api_key = openai_image.load_api_key()
    client = openai_image.build_client(api_key)
    png_images = openai_image.request_images(client, context.prompt_config)
    if not png_images:
        raise RuntimeError("OpenAI Images API returned no images")
    if len(png_images) > 1:
        logger.warning(
            "動画方式は先頭画像のみ使用: prompt_config_id=%s count=%s",
            context.prompt_config.id,
            len(png_images),
        )
    jpeg = openai_image.convert_png_to_jpeg(png_images[0])

    audio_asset_id, audio_s3_key = _select_audio_asset(
        context.cursor, context.prompt_config.set_id
    )
    logger.info(
        "音源を選曲: audio_asset_id=%s s3_key=%s",
        audio_asset_id,
        audio_s3_key,
    )
    audio = get_object(
        context.s3_bucket,
        audio_s3_key,
        client=context.s3_client,
    )
    video = _build_video(_compose_canvas(jpeg), audio)
    context.cursor.execute(
        "UPDATE audio_assets SET last_used_at = %s WHERE id = %s",
        (now_utc(), audio_asset_id),
    )

    return GeneratorResult(
        media=[
            MediaOutput(
                content=video,
                file_format="mp4",
                width=OUTPUT_WIDTH,
                height=OUTPUT_HEIGHT,
                duration_seconds=OUTPUT_DURATION_SECONDS,
                audio_asset_id=audio_asset_id,
            )
        ],
        intermediates=[
            IntermediateOutput(
                content=jpeg,
                file_format="jpg",
                suffix="_source",
                output_index=0,
            )
        ],
    )
