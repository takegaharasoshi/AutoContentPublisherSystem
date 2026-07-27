"""Final-media generator contracts."""

from collections.abc import Callable
from dataclasses import dataclass, field
import datetime
from typing import Any

from ..models import PromptConfig


@dataclass(frozen=True)
class MediaOutput:
    """One final, publishable media object returned by a generator."""

    content: bytes
    file_format: str
    width: int | None = None
    height: int | None = None
    duration_seconds: int | None = None
    audio_asset_id: int | None = None


@dataclass(frozen=True)
class IntermediateOutput:
    """An intermediate artifact stored only in S3."""

    content: bytes
    file_format: str
    suffix: str
    output_index: int


@dataclass(frozen=True)
class GeneratorResult:
    """Final media and optional intermediate artifacts."""

    media: list[MediaOutput]
    intermediates: list[IntermediateOutput] = field(default_factory=list)


@dataclass(frozen=True)
class GeneratorContext:
    """Execution dependencies supplied to a generator."""

    prompt_config: PromptConfig
    cursor: Any
    s3_client: Any
    s3_bucket: str
    scheduled_at: datetime.datetime
    generation_run_id: int


GeneratorFn = Callable[[GeneratorContext], GeneratorResult]


class GeneratorNotFoundError(Exception):
    """Raised when a batch set references an unknown generator."""
