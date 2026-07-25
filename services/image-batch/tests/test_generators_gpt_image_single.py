"""Tests for the OpenAI GPT Image final-image generator."""

from io import BytesIO
import json
from unittest.mock import Mock

from PIL import Image

from app.generators import GeneratorContext
from app.generators import gpt_image_single
from app.models import PromptConfig


def _prompt_config() -> PromptConfig:
    """Create a prompt configuration for generator tests."""
    return PromptConfig(
        1,
        1,
        "A sunset over the ocean",
        "rain",
        json.dumps(
            {
                "model": "gpt-image-2",
                "size": "1024x1024",
                "quality": "high",
                "n": 1,
            }
        ),
    )


def _jpeg_bytes(width: int, height: int) -> bytes:
    """Create a small JPEG fixture."""
    output = BytesIO()
    Image.new("RGB", (width, height), "blue").save(output, format="JPEG")
    return output.getvalue()


def test_generate_returns_jpeg_dimensions(
    monkeypatch,
) -> None:
    """The final media contract includes dimensions read from the JPEG."""
    calls: list[tuple[str, object]] = []
    client = object()
    jpeg = _jpeg_bytes(6, 10)
    prompt_config = _prompt_config()
    context = GeneratorContext(prompt_config, Mock(), Mock(), "bucket")

    monkeypatch.setattr(
        gpt_image_single.openai_image,
        "load_api_key",
        lambda: calls.append(("load", None)) or "test-key",
    )
    monkeypatch.setattr(
        gpt_image_single.openai_image,
        "build_client",
        lambda key: calls.append(("build", key)) or client,
    )
    monkeypatch.setattr(
        gpt_image_single.openai_image,
        "request_images",
        lambda received_client, prompt: calls.append(
            ("request", (received_client, prompt))
        )
        or [b"png"],
    )
    monkeypatch.setattr(
        gpt_image_single.openai_image,
        "convert_png_to_jpeg",
        lambda png: calls.append(("convert", png)) or jpeg,
    )

    result = gpt_image_single.generate(context)

    assert len(result.media) == 1
    assert result.intermediates == []
    assert result.media[0].content == jpeg
    assert result.media[0].file_format == "jpg"
    assert result.media[0].width == 6
    assert result.media[0].height == 10
    assert result.media[0].duration_seconds is None
    assert calls == [
        ("load", None),
        ("build", "test-key"),
        ("request", (client, prompt_config)),
        ("convert", b"png"),
    ]
