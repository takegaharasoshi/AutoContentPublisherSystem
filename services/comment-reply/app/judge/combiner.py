"""Compose supported judge modes without duplicating their classifiers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping

from app.config import Config
from app.judge import haiku, jev, luna
from app.judge.contract import Judgement, Problem


Outcome = Judgement | Exception
FALLBACK_METHODS = {"haiku": "luna", "luna": "haiku", "jev": "haiku"}


@dataclass(frozen=True)
class Combined:
    """All observed judge results and the decision used by the writer."""

    luna: Judgement | None
    jev: Judgement | None
    kind: str
    answer: str | None
    bare_term: str | None
    decision: str
    errors: list[str] = field(default_factory=list)
    haiku: Judgement | None = None

    def final_log(self) -> dict[str, str | None]:
        """Return the stable final-decision log object."""
        return {"kind": self.kind, "answer": self.answer, "decision": self.decision}


def combine(
    comment_id: str, text: str, problem: Problem, config: Config,
    credentials: Mapping[str, str], *,
    precomputed: Mapping[str, Outcome] | None = None,
    luna_call: Callable[..., Judgement] = luna.judge,
    jev_call: Callable[..., Judgement] = jev.judge,
    haiku_call: Callable[..., Judgement] = haiku.judge,
) -> Combined:
    """Call the main judge first and its fallback only after a failure."""
    main = config.judge_mode
    if main not in FALLBACK_METHODS:
        raise ValueError(f"invalid JUDGE_MODE: {main}")
    supplied = precomputed or {}
    calls = {"luna": luna_call, "jev": jev_call, "haiku": haiku_call}
    observed: dict[str, Judgement] = {}
    errors: list[str] = []

    def call(method: str) -> Judgement:
        try:
            if method in supplied:
                outcome = supplied[method]
            else:
                kwargs = {
                    "luna": {"api_key": credentials.get("openai_api_key", ""),
                             "model": config.luna_model, "effort": config.luna_effort},
                    "jev": {"api_key": credentials.get("typesafe_api_key", "")},
                    "haiku": {"api_key": credentials.get("anthropic_api_key", ""),
                              "effort": config.haiku_effort},
                }[method]
                outcome = calls[method](comment_id, text, problem, **kwargs)
            if isinstance(outcome, Exception):
                raise outcome
            if not isinstance(outcome, Judgement):
                raise TypeError(f"{method} returned no judgement")
        except Exception as exc:
            outcome = Judgement(
                method, None, error=str(exc) or type(exc).__name__,
                debug=getattr(exc, "debug", {}),
            )
        observed[method] = outcome
        if outcome.error is not None:
            errors.append(f"{method}: {outcome.error}")
        return outcome

    chosen = call(main)
    decision = main
    if chosen.error is not None:
        fallback = FALLBACK_METHODS[main]
        chosen = call(fallback)
        if chosen.error is not None:
            raise RuntimeError("both judges failed: " + "; ".join(errors))
        decision = f"{main}_fallback_{fallback}"
    return Combined(
        luna=observed.get("luna"), jev=observed.get("jev"), haiku=observed.get("haiku"),
        kind=chosen.kind or "", answer=chosen.answer, bare_term=chosen.bare_term,
        decision=decision, errors=errors,
    )
