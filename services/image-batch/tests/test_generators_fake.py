"""Tests for the fake generator."""

from app.generators.fake import generate
from app.models import PromptConfig


def test_fake_generator_returns_one_fixed_payload() -> None:
    """The local fake implementation is deterministic."""
    prompt_config = PromptConfig(1, 1, "prompt", None, None)

    assert generate(prompt_config) == [b"fake-image-bytes-for-local-e2e-testing"]
