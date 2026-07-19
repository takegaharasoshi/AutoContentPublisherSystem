"""OpenAI GPT Image single-request generator."""

from __future__ import annotations

import base64
from io import BytesIO
import json
import os
from typing import Any

import openai
from PIL import Image

from acps_shared import get_secret_string

from ..models import PromptConfig


def _load_api_key() -> str:
    """Retrieve the OpenAI API key from the configured secret.

    Returns:
        The API key stored in the Secrets Manager JSON value.
    """
    secret_arn = os.environ["API_SECRET_ARN"]
    secret_string = get_secret_string(secret_arn)
    return json.loads(secret_string)["api_key"]


def _build_client(api_key: str) -> "openai.OpenAI":
    """Construct an OpenAI SDK client with a request timeout.

    Args:
        api_key: API key used to authenticate to OpenAI.

    Returns:
        Configured OpenAI SDK client.
    """
    return openai.OpenAI(api_key=api_key, timeout=300.0)


def _request_images(client: Any, prompt_config: PromptConfig) -> list[bytes]:
    """Generate PNG images using parameters stored in the prompt configuration.

    Args:
        client: OpenAI SDK client.
        prompt_config: Prompt configuration containing generation parameters.

    Returns:
        Generated PNG image payloads.
    """
    params = json.loads(prompt_config.parameters)
    response = client.images.generate(
        model=params["model"],
        prompt=prompt_config.prompt_text,
        size=params["size"],
        quality=params["quality"],
        n=params["n"],
    )
    return [base64.b64decode(image.b64_json) for image in response.data]


def _convert_png_to_jpeg(png_bytes: bytes, *, quality: int = 90) -> bytes:
    """Convert a PNG image payload to JPEG bytes.

    Args:
        png_bytes: PNG image data to convert.
        quality: JPEG encoder quality.

    Returns:
        JPEG image data.
    """
    with Image.open(BytesIO(png_bytes)) as image:
        jpeg_image = image if image.mode == "RGB" else image.convert("RGB")
        output = BytesIO()
        jpeg_image.save(output, format="JPEG", quality=quality)
    return output.getvalue()


def generate(prompt_config: PromptConfig) -> list[bytes]:
    """Generate JPEG images from one prompt configuration.

    Args:
        prompt_config: Prompt configuration to generate from.

    Returns:
        Generated JPEG image payloads.
    """
    api_key = _load_api_key()
    client = _build_client(api_key)
    png_images = _request_images(client, prompt_config)
    return [_convert_png_to_jpeg(png_image) for png_image in png_images]
