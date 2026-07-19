"""Tests for the generator registry."""

import pytest

from app.generators import GeneratorNotFoundError, REGISTRY, resolve_generator
from app.generators import gpt_image_single


def test_resolve_generator_returns_registered_generator() -> None:
    """The fake generator can be resolved by its configured name."""
    assert resolve_generator("fake") is REGISTRY["fake"]


def test_resolve_generator_returns_gpt_image_single_generator() -> None:
    """The GPT Image generator can be resolved by its configured name."""
    assert resolve_generator("gpt-image-single") is gpt_image_single.generate


def test_resolve_generator_rejects_unknown_name() -> None:
    """Unknown configuration names are reported without fallback."""
    with pytest.raises(GeneratorNotFoundError, match="missing-generator"):
        resolve_generator("missing-generator")
