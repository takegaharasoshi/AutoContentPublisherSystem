"""Shared immutable data contract for production judging."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
import unicodedata


KINDS = (
    "q_yesno", "q_multi", "q_open", "guess_correct", "guess_close",
    "guess_wrong", "ask_hint", "ask_spoiler", "ask_howto", "impression",
    "greeting", "cheer", "chat", "request", "complaint", "mention",
    "emoji_only", "troll", "abuse", "spam", "personal_info", "foreign",
)
ANSWERS = frozenset({"yes", "no", "irrelevant"})


def bare_term_text(text: str) -> str:
    """Preserve the comment's wording while removing surrounding symbols."""
    term = text.strip()
    while term and (term[0].isspace() or unicodedata.category(term[0])[0] in {"P", "S"}):
        term = term[1:]
    while term and (term[-1].isspace() or unicodedata.category(term[-1])[0] in {"P", "S"}):
        term = term[:-1]
    return term


class ProblemInvalid(ValueError):
    """The published problem snapshot is missing required judge data."""


@dataclass(frozen=True)
class JudgeCriteria:
    """Immutable hit/touch boundaries and examples of disqualifying errors."""

    points: tuple[tuple[str, str], ...]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class Problem:
    """One published snapshot, kept separate from the stock authoring format."""

    schema_version: int
    set_code: str
    media_id: str
    content_key: str
    problem_text: str
    truth: str
    fact_sheet: tuple[str, ...]
    core_points: tuple[str, ...]
    judge_criteria: JudgeCriteria
    reveal_text: str

    @classmethod
    def from_snapshot(cls, raw: Mapping[str, Any]) -> Problem:
        """Validate and build a problem from schema version 3 or later."""
        if not isinstance(raw, Mapping):
            raise ProblemInvalid("snapshot must be an object")
        version = raw.get("schema_version")
        if not isinstance(version, int) or isinstance(version, bool) or version < 3:
            raise ProblemInvalid("schema_version must be >= 3")
        fields = ("set_code", "media_id", "content_key", "problem_text", "truth", "reveal_text")
        for key in fields:
            if not isinstance(raw.get(key), str) or not raw[key].strip():
                raise ProblemInvalid(f"{key} is missing or empty")
        for key in ("fact_sheet", "core_points"):
            value = raw.get(key)
            if not isinstance(value, list) or not value or any(
                not isinstance(item, str) or not item.strip() for item in value
            ):
                raise ProblemInvalid(f"{key} must be a nonempty string array")
        criteria = raw.get("judge_criteria")
        if not isinstance(criteria, Mapping):
            raise ProblemInvalid("judge_criteria must be an object")
        points = criteria.get("points")
        if not isinstance(points, list) or len(points) != len(raw["core_points"]):
            raise ProblemInvalid("judge_criteria.points must match core_points")
        parsed_points = []
        for point in points:
            if not isinstance(point, Mapping) or any(
                not isinstance(point.get(key), str) or not point[key].strip()
                for key in ("hit", "touch")
            ):
                raise ProblemInvalid("judge_criteria.points require nonempty hit and touch")
            parsed_points.append((point["hit"], point["touch"]))
        errors = criteria.get("errors")
        if (
            not isinstance(errors, list)
            or len(errors) > 3
            or any(not isinstance(error, str) or not error.strip() for error in errors)
        ):
            raise ProblemInvalid("judge_criteria.errors must be 0 to 3 nonempty strings")
        return cls(
            schema_version=version,
            set_code=raw["set_code"], media_id=raw["media_id"],
            content_key=raw["content_key"], problem_text=raw["problem_text"],
            truth=raw["truth"], fact_sheet=tuple(raw["fact_sheet"]),
            core_points=tuple(raw["core_points"]),
            judge_criteria=JudgeCriteria(tuple(parsed_points), tuple(errors)),
            reveal_text=raw["reveal_text"],
        )


@dataclass(frozen=True)
class Judgement:
    """One method's decision; an error result has kind=None and error set."""

    method: str
    kind: str | None
    answer: str | None = None
    reason: str = ""
    bare_term: str | None = None
    reply_draft: str | None = None
    debug: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def __post_init__(self) -> None:
        if self.method not in {"luna", "jev", "decisions", "haiku"}:
            raise ValueError("invalid judgement method")
        if self.error is None and self.kind not in KINDS:
            raise ValueError(f"invalid judgement kind: {self.kind}")
        if self.kind == "q_yesno" and self.answer not in ANSWERS:
            raise ValueError("q_yesno requires an answer")
        if self.kind != "q_yesno" and self.answer is not None:
            raise ValueError("only q_yesno can have an answer")

    def as_log(self) -> dict[str, Any]:
        """Return the compact, stable log shape without the draft text."""
        return {
            "kind": self.kind, "answer": self.answer, "reason": self.reason,
            "bare_term": self.bare_term, "error": self.error, "debug": self.debug,
        }
