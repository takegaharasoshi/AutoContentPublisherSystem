"""Data models used by the image batch."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BatchSet:
    """A batch set selected for image generation."""

    id: int
    set_code: str
    generator_name: str
    is_active: bool


@dataclass(frozen=True)
class PromptConfig:
    """An active image-generation prompt configuration."""

    id: int
    set_id: int
    prompt_text: str
    negative_prompt: str | None
    parameters: str | None
