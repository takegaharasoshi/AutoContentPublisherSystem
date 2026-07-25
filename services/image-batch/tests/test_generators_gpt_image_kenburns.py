"""Tests for the GPT Image Ken Burns video generator."""

import datetime
import logging
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.generators import GeneratorContext
from app.generators import gpt_image_kenburns
from app.models import PromptConfig


class FakeCursor:
    """Cursor fake for audio selection and update tracking."""

    def __init__(self, audio_row=(7, "audio/set-a/track.m4a")) -> None:
        """Initialize SQL tracking and selected row."""
        self.audio_row = audio_row
        self.calls: list[tuple[str, tuple]] = []
        self.commit = Mock()

    def execute(self, sql: str, params: tuple) -> None:
        """Record executed SQL."""
        self.calls.append((sql, params))

    def fetchone(self):
        """Return the configured selection row."""
        return self.audio_row


def _context(cursor: FakeCursor) -> GeneratorContext:
    """Create a generator context."""
    return GeneratorContext(
        PromptConfig(
            3,
            11,
            "vertical scene",
            None,
            '{"model":"gpt-image-2","size":"1024x1536",'
            '"quality":"high","n":1}',
        ),
        cursor,
        Mock(),
        "bucket",
    )


def _patch_generation_dependencies(monkeypatch, *, video=b"mp4") -> None:
    """Patch API, S3, encoding, and clock dependencies."""
    monkeypatch.setattr(
        gpt_image_kenburns.openai_image, "load_api_key", lambda: "key"
    )
    monkeypatch.setattr(
        gpt_image_kenburns.openai_image, "build_client", lambda key: object()
    )
    monkeypatch.setattr(
        gpt_image_kenburns.openai_image,
        "request_images",
        lambda client, prompt: [b"png"],
    )
    monkeypatch.setattr(
        gpt_image_kenburns.openai_image,
        "convert_png_to_jpeg",
        lambda png: b"jpeg",
    )
    monkeypatch.setattr(
        gpt_image_kenburns, "get_object", lambda *args, **kwargs: b"aac"
    )
    monkeypatch.setattr(
        gpt_image_kenburns, "_build_video", lambda jpeg, audio: video
    )
    monkeypatch.setattr(
        gpt_image_kenburns,
        "now_utc",
        lambda: datetime.datetime(2026, 7, 25, 1, 2, 3),
    )


def test_generate_rotates_audio_and_returns_audio_asset_id(
    monkeypatch,
    caplog,
) -> None:
    """Selection SQL, update, and output metadata use the chosen asset."""
    cursor = FakeCursor()
    _patch_generation_dependencies(monkeypatch)

    with caplog.at_level(logging.INFO):
        result = gpt_image_kenburns.generate(_context(cursor))

    select_sql, select_params = cursor.calls[0]
    assert "WHERE set_id = %s AND is_active = 1" in select_sql
    assert "ORDER BY last_used_at ASC, id ASC LIMIT 1" in select_sql
    assert select_params == (11,)
    update_sql, update_params = cursor.calls[1]
    assert update_sql == "UPDATE audio_assets SET last_used_at = %s WHERE id = %s"
    assert update_params == (datetime.datetime(2026, 7, 25, 1, 2, 3), 7)
    assert "audio_asset_id=7 s3_key=audio/set-a/track.m4a" in caplog.text
    cursor.commit.assert_not_called()
    assert result.media[0].audio_asset_id == 7
    assert result.media[0].file_format == "mp4"
    assert (result.media[0].width, result.media[0].height) == (1080, 1920)
    assert result.media[0].duration_seconds == 10
    assert result.intermediates[0].suffix == "_source"
    assert result.intermediates[0].output_index == 0


def test_generate_fails_when_no_active_audio(monkeypatch) -> None:
    """A set without active audio is a loud configuration error."""
    cursor = FakeCursor(audio_row=None)
    _patch_generation_dependencies(monkeypatch)

    with pytest.raises(RuntimeError, match="No active audio_assets"):
        gpt_image_kenburns.generate(_context(cursor))

    assert len(cursor.calls) == 1
    cursor.commit.assert_not_called()


def test_build_video_invokes_ffmpeg_with_required_parameters(
    monkeypatch,
) -> None:
    """Encoding uses the fixed dimensions, duration, codec, and copied AAC."""
    observed: dict[str, object] = {}

    def run(command, **kwargs):
        observed["command"] = command
        observed.update(kwargs)
        Path(command[-1]).write_bytes(b"video")

    monkeypatch.setattr(gpt_image_kenburns.subprocess, "run", run)
    monkeypatch.setattr(gpt_image_kenburns, "FFMPEG_BINARY", "test-ffmpeg")

    assert gpt_image_kenburns._build_video(b"jpeg", b"aac") == b"video"

    command = observed["command"]
    assert command[0] == "test-ffmpeg"
    assert command[command.index("-filter_complex") + 1] == (
        "[0:v]scale=-2:1920,crop=1080:1920,scale=2160:3840,"
        "zoompan=z='1.0+0.08*on/299':x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
        "format=yuv420p[v]"
    )
    assert command[command.index("-crf") + 1] == "20"
    assert command[command.index("-c:a") + 1] == "copy"
    assert command.count("-t") == 2
    duration_values = [
        command[index + 1]
        for index, value in enumerate(command)
        if value == "-t"
    ]
    assert duration_values == ["10", "10"]
    assert observed["check"] is True
    assert observed["capture_output"] is True
    assert observed["timeout"] == 600


def test_zoompan_filter_uses_output_constants(monkeypatch) -> None:
    """Dimensions, frame count, and supersampling derive from constants."""
    monkeypatch.setattr(gpt_image_kenburns, "OUTPUT_WIDTH", 200)
    monkeypatch.setattr(gpt_image_kenburns, "OUTPUT_HEIGHT", 300)
    monkeypatch.setattr(gpt_image_kenburns, "OUTPUT_FPS", 5)
    monkeypatch.setattr(gpt_image_kenburns, "OUTPUT_DURATION_SECONDS", 4)
    monkeypatch.setattr(gpt_image_kenburns, "ZOOM_END", 1.12)

    assert gpt_image_kenburns._build_zoompan_filter() == (
        "[0:v]scale=-2:300,crop=200:300,scale=400:600,"
        "zoompan=z='1.0+0.12*on/19':x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)':d=1:s=200x300:fps=5,"
        "format=yuv420p[v]"
    )


def test_build_video_rejects_empty_output(monkeypatch) -> None:
    """A successful ffmpeg exit cannot return an empty media payload."""
    def run(command, **kwargs):
        del kwargs
        Path(command[-1]).write_bytes(b"")

    monkeypatch.setattr(gpt_image_kenburns.subprocess, "run", run)
    with pytest.raises(RuntimeError, match="empty"):
        gpt_image_kenburns._build_video(b"jpeg", b"aac")
