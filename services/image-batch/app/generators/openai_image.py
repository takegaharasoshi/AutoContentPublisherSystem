"""Shared OpenAI Images API helpers."""

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


def load_api_key() -> str:
    """Retrieve the OpenAI API key from the configured secret."""
    secret_arn = os.environ["API_SECRET_ARN"]
    secret_string = get_secret_string(secret_arn)
    return json.loads(secret_string)["api_key"]


def build_client(api_key: str) -> "openai.OpenAI":
    """Construct an OpenAI SDK client with a request timeout."""
    return openai.OpenAI(api_key=api_key, timeout=300.0)


def request_images(client: Any, prompt_config: PromptConfig) -> list[bytes]:
    """Generate and decode PNG images for a prompt configuration."""
    params = json.loads(prompt_config.parameters)
    response = client.images.generate(
        model=params["model"],
        prompt=prompt_config.prompt_text,
        size=params["size"],
        quality=params["quality"],
        n=params["n"],
    )
    return [base64.b64decode(image.b64_json) for image in response.data]


def request_illustration(client: Any, prompt: str) -> bytes:
    """Generate and decode one medium-quality landscape PNG illustration."""
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024",
        quality="medium",
        n=1,
    )
    data = getattr(response, "data", None)
    if not data:
        raise RuntimeError("OpenAI Images API returned no illustration")
    encoded = getattr(data[0], "b64_json", None)
    if not isinstance(encoded, str) or not encoded:
        raise RuntimeError(
            "OpenAI Images API illustration did not contain PNG data"
        )
    return base64.b64decode(encoded)


def convert_png_to_jpeg(png_bytes: bytes, *, quality: int = 90) -> bytes:
    """Convert PNG bytes to RGB JPEG bytes."""
    with Image.open(BytesIO(png_bytes)) as image:
        jpeg_image = image if image.mode == "RGB" else image.convert("RGB")
        output = BytesIO()
        jpeg_image.save(output, format="JPEG", quality=quality)
    return output.getvalue()
