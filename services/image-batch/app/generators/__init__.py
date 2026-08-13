"""Final-media generator contracts and registry."""

from .contracts import (
    GeneratorContext,
    GeneratorFn,
    GeneratorNotFoundError,
    GeneratorResult,
    IntermediateOutput,
    MediaOutput,
)
from . import (
    fake,
    gpt_image_kenburns,
    gpt_image_single,
    gpt_quiz_multicut,
    quiz_prebuilt,
    ranking_prebuilt,
)


__all__ = [
    "GeneratorContext",
    "GeneratorFn",
    "GeneratorNotFoundError",
    "GeneratorResult",
    "IntermediateOutput",
    "MediaOutput",
    "REGISTRY",
    "resolve_generator",
]


REGISTRY: dict[str, GeneratorFn] = {
    "fake": fake.generate,
    "gpt-image-kenburns": gpt_image_kenburns.generate,
    "gpt-image-single": gpt_image_single.generate,
    "gpt-quiz-multicut": gpt_quiz_multicut.generate,
    "quiz-prebuilt": quiz_prebuilt.generate,
    "ranking-prebuilt": ranking_prebuilt.generate,
}


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
