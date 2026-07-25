"""Local-only fake image generator."""

from .contracts import GeneratorContext, GeneratorResult, MediaOutput


def generate(context: GeneratorContext) -> GeneratorResult:
    """Return one fixed fake final image for local and E2E tests."""
    del context
    return GeneratorResult(
        media=[
            MediaOutput(
                content=b"fake-image-bytes-for-local-e2e-testing",
                file_format="jpg",
            )
        ]
    )
