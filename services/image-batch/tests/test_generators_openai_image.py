"""Tests for shared OpenAI Images API helpers."""

import base64
from io import BytesIO
import json
from types import SimpleNamespace
from typing import Any

from PIL import Image
import pytest

from app.generators import openai_image
from app.models import PromptConfig


def _prompt_config(parameters: str | None = None) -> PromptConfig:
    """Create a prompt configuration for helper tests."""
    return PromptConfig(
        1,
        1,
        "A sunset over the ocean",
        "rain",
        parameters
        or json.dumps(
            {
                "model": "gpt-image-2",
                "size": "1024x1024",
                "quality": "high",
                "n": 1,
            }
        ),
    )


def _png_bytes(mode: str = "RGB") -> bytes:
    """Create a small PNG fixture."""
    color = (10, 20, 30, 128) if mode == "RGBA" else (10, 20, 30)
    image = Image.new(mode, (2, 2), color)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def test_load_api_key_reads_secret_json(monkeypatch) -> None:
    """The API key is read from the configured secret."""
    monkeypatch.setenv("API_SECRET_ARN", "arn:secret")
    monkeypatch.setattr(
        openai_image,
        "get_secret_string",
        lambda arn: '{"api_key":"test-key"}',
    )

    assert openai_image.load_api_key() == "test-key"


def test_build_client_passes_api_key_and_timeout(monkeypatch) -> None:
    """The SDK client receives the configured timeout."""
    observed: dict[str, Any] = {}
    expected = object()

    def constructor(**kwargs):
        observed.update(kwargs)
        return expected

    monkeypatch.setattr(openai_image.openai, "OpenAI", constructor)
    assert openai_image.build_client("key") is expected
    assert observed == {"api_key": "key", "timeout": 300.0}


def test_request_images_passes_parameters_and_decodes() -> None:
    """Stored parameters are forwarded and base64 payloads decoded."""
    expected = [b"one", b"two"]
    response = SimpleNamespace(
        data=[
            SimpleNamespace(b64_json=base64.b64encode(value).decode())
            for value in expected
        ]
    )
    observed: dict[str, Any] = {}
    client = SimpleNamespace(
        images=SimpleNamespace(
            generate=lambda **kwargs: observed.update(kwargs) or response
        )
    )

    assert openai_image.request_images(client, _prompt_config()) == expected
    assert observed == {
        "model": "gpt-image-2",
        "prompt": "A sunset over the ocean",
        "size": "1024x1024",
        "quality": "high",
        "n": 1,
    }


def test_request_images_rejects_missing_parameter() -> None:
    """Missing required generation parameters fail loudly."""
    client = SimpleNamespace(images=SimpleNamespace(generate=lambda **_: None))
    with pytest.raises(KeyError, match="size"):
        openai_image.request_images(
            client, _prompt_config('{"model":"gpt-image-2"}')
        )


@pytest.mark.parametrize("mode", ["RGB", "RGBA"])
def test_convert_png_to_jpeg(mode: str) -> None:
    """RGB and transparent PNGs become valid RGB JPEGs."""
    jpeg = openai_image.convert_png_to_jpeg(_png_bytes(mode))
    with Image.open(BytesIO(jpeg)) as image:
        assert image.format == "JPEG"
        assert image.mode == "RGB"
        assert image.size == (2, 2)
