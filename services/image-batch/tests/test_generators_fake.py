"""Tests for the fake generator."""

from unittest.mock import Mock

from app.generators import GeneratorContext, GeneratorResult, MediaOutput
from app.generators.fake import generate
from app.models import PromptConfig


def test_fake_generator_returns_one_fixed_payload() -> None:
    """The local fake implementation is deterministic."""
    prompt_config = PromptConfig(1, 1, "prompt", None, None)

    context = GeneratorContext(prompt_config, Mock(), Mock(), "bucket")
    assert generate(context) == GeneratorResult(
        [MediaOutput(b"fake-image-bytes-for-local-e2e-testing", "jpg")]
    )
