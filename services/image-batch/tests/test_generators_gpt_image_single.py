"""Tests for the OpenAI GPT Image single-request generator."""

import base64
from io import BytesIO
import json
from types import SimpleNamespace
from typing import Any

import pytest
from PIL import Image

from app.generators import gpt_image_single
from app.models import PromptConfig


def _prompt_config(parameters: str | None = None) -> PromptConfig:
    """Create a prompt configuration for generator tests."""
    return PromptConfig(
        id=1,
        set_id=1,
        prompt_text="A sunset over the ocean",
        negative_prompt="rain",
        parameters=parameters
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
    """Create a small PNG fixture with the requested color mode."""
    image = Image.new(mode, (2, 2), (10, 20, 30, 128) if mode == "RGBA" else 0)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def test_load_api_key_reads_secret_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The API key is read from the configured Secrets Manager secret."""
    observed: dict[str, str] = {}
    monkeypatch.setenv("API_SECRET_ARN", "arn:aws:secretsmanager:example")

    def get_secret_string(secret_arn: str) -> str:
        observed["secret_arn"] = secret_arn
        return '{"api_key":"test-key"}'

    monkeypatch.setattr(
        gpt_image_single, "get_secret_string", get_secret_string
    )

    assert gpt_image_single._load_api_key() == "test-key"
    assert observed == {"secret_arn": "arn:aws:secretsmanager:example"}


def test_build_client_passes_api_key_and_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The SDK client receives the API key and explicit request timeout."""
    observed: dict[str, Any] = {}
    expected_client = object()

    def openai_constructor(**kwargs: Any) -> object:
        observed.update(kwargs)
        return expected_client

    monkeypatch.setattr(gpt_image_single.openai, "OpenAI", openai_constructor)

    assert gpt_image_single._build_client("test-key") is expected_client
    assert observed == {"api_key": "test-key", "timeout": 300.0}


def test_request_images_uses_prompt_parameters_and_decodes_images() -> None:
    """Stored generation parameters are passed through and images decode."""
    image_bytes = [b"first-png", b"second-png"]
    response = SimpleNamespace(
        data=[
            SimpleNamespace(b64_json=base64.b64encode(value).decode())
            for value in image_bytes
        ]
    )
    observed: dict[str, Any] = {}

    def generate(**kwargs: Any) -> Any:
        observed.update(kwargs)
        return response

    client = SimpleNamespace(images=SimpleNamespace(generate=generate))
    prompt_config = _prompt_config()

    actual_images = gpt_image_single._request_images(client, prompt_config)

    assert actual_images == image_bytes
    assert observed == {
        "model": "gpt-image-2",
        "prompt": "A sunset over the ocean",
        "size": "1024x1024",
        "quality": "high",
        "n": 1,
    }


def test_request_images_rejects_missing_required_parameter() -> None:
    """A missing generation parameter propagates as a configuration error."""
    client = SimpleNamespace(images=SimpleNamespace(generate=lambda **_: None))
    prompt_config = _prompt_config('{"model":"gpt-image-2"}')

    with pytest.raises(KeyError, match="size"):
        gpt_image_single._request_images(client, prompt_config)


@pytest.mark.parametrize("mode", ["RGB", "RGBA"])
def test_convert_png_to_jpeg_returns_valid_jpeg(mode: str) -> None:
    """RGB and transparent PNG images are converted to valid JPEG data."""
    jpeg_bytes = gpt_image_single._convert_png_to_jpeg(_png_bytes(mode))

    with Image.open(BytesIO(jpeg_bytes)) as image:
        assert image.format == "JPEG"
        assert image.mode == "RGB"
        assert image.size == (2, 2)


def test_generate_orchestrates_internal_steps(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Generation loads credentials, requests PNGs, then converts images."""
    calls: list[tuple[str, Any]] = []
    client = object()
    prompt_config = _prompt_config()

    monkeypatch.setattr(
        gpt_image_single,
        "_load_api_key",
        lambda: calls.append(("load", None)) or "test-key",
    )
    monkeypatch.setattr(
        gpt_image_single,
        "_build_client",
        lambda api_key: calls.append(("build", api_key)) or client,
    )
    monkeypatch.setattr(
        gpt_image_single,
        "_request_images",
        lambda received_client, received_prompt: calls.append(
            ("request", (received_client, received_prompt))
        )
        or [b"one", b"two"],
    )

    def convert(png_bytes: bytes) -> bytes:
        calls.append(("convert", png_bytes))
        return b"jpeg-" + png_bytes

    monkeypatch.setattr(gpt_image_single, "_convert_png_to_jpeg", convert)

    actual_images = gpt_image_single.generate(prompt_config)

    assert actual_images == [b"jpeg-one", b"jpeg-two"]
    assert calls == [
        ("load", None),
        ("build", "test-key"),
        ("request", (client, prompt_config)),
        ("convert", b"one"),
        ("convert", b"two"),
    ]
