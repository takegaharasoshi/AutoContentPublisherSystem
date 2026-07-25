"""OpenAI GPT Image final-image generator."""

from __future__ import annotations

from io import BytesIO

from PIL import Image

from . import openai_image
from .contracts import GeneratorContext, GeneratorResult, MediaOutput


def generate(context: GeneratorContext) -> GeneratorResult:
    """Generate final JPEG images from one prompt configuration."""
    api_key = openai_image.load_api_key()
    client = openai_image.build_client(api_key)
    png_images = openai_image.request_images(client, context.prompt_config)
    media = []
    for png_image in png_images:
        jpeg = openai_image.convert_png_to_jpeg(png_image)
        with Image.open(BytesIO(jpeg)) as image:
            width, height = image.size
        media.append(
            MediaOutput(
                content=jpeg,
                file_format="jpg",
                width=width,
                height=height,
            )
        )
    return GeneratorResult(media=media)
