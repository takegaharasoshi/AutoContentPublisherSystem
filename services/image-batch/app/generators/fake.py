"""Local-only fake image generator."""

from ..models import PromptConfig


def generate(prompt_config: PromptConfig) -> list[bytes]:
    """Return one fixed fake image payload for local and E2E tests.

    Args:
        prompt_config: Prompt configuration to generate from.

    Returns:
        A single non-image byte payload. No real image generation occurs.
    """
    del prompt_config
    return [b"fake-image-bytes-for-local-e2e-testing"]
