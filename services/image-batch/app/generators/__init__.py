"""Image generator registry."""

from collections.abc import Callable

from ..models import PromptConfig
from . import fake


GeneratorFn = Callable[[PromptConfig], list[bytes]]


class GeneratorNotFoundError(Exception):
    """Raised when a batch set references an unknown generator."""


REGISTRY: dict[str, GeneratorFn] = {"fake": fake.generate}


def resolve_generator(generator_name: str) -> GeneratorFn:
    """Resolve a generator by name.

    Args:
        generator_name: Registry key configured on the batch set.

    Returns:
        The resolved generator.

    Raises:
        GeneratorNotFoundError: If the registry has no such generator.
    """
    try:
        return REGISTRY[generator_name]
    except KeyError:
        raise GeneratorNotFoundError(
            f"Generator is not registered: {generator_name}"
        ) from None
