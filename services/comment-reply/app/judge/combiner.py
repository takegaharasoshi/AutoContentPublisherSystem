"""Compose supported judge modes without duplicating their classifiers."""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Callable, Mapping

from app.config import Config
from app.judge import decisions, haiku, jev, luna
from app.judge.contract import Judgement, Problem


LOGGER = logging.getLogger(__name__)
Outcome = Judgement | Exception


@dataclass(frozen=True)
class Combined:
    """All observed judge results and the decision used by the writer."""

    luna: Judgement | None
    jev: Judgement | None
    kind: str
    answer: str | None
    bare_term: str | None
    decision: str
    mismatch: bool | None
    errors: list[str] = field(default_factory=list)
    decisions: Judgement | None = None
    haiku: Judgement | None = None

    def final_log(self) -> dict[str, str | None]:
        """Return the stable final-decision log object."""
        return {"kind": self.kind, "answer": self.answer, "decision": self.decision}


def combine(
    comment_id: str, text: str, problem: Problem, config: Config,
    credentials: Mapping[str, str], *,
    media_id: str | None = None,
    precomputed: Mapping[str, Outcome] | None = None,
    luna_call: Callable[..., Judgement] = luna.judge,
    jev_call: Callable[..., Judgement] = jev.judge,
    decisions_call: Callable[..., Judgement] = decisions.judge,
    haiku_call: Callable[..., Judgement] = haiku.judge,
) -> Combined:
    """Choose a mode, with optional precomputed local-trial calls."""
    supplied = precomputed or {}
    need_jev = config.judge_mode == "jev" or (
        config.judge_mode == "hybrid" and (config.shadow or config.consensus)
    )
    need_luna = config.judge_mode != "jev"

    def call_luna() -> Outcome:
        if "luna" in supplied:
            return supplied["luna"]
        try:
            return luna_call(
                comment_id, text, problem, api_key=credentials.get("openai_api_key", ""),
                model=config.luna_model,
            )
        except Exception as exc:
            return exc

    def call_jev() -> Outcome:
        if "jev" in supplied:
            return supplied["jev"]
        try:
            return jev_call(
                comment_id, text, problem, api_key=credentials.get("typesafe_api_key", ""),
            )
        except Exception as exc:
            return exc

    if config.judge_mode in {"decisions", "haiku"}:
        method = config.judge_mode
        if method in supplied:
            outcome = supplied[method]
        else:
            try:
                if method == "haiku":
                    outcome = haiku_call(
                        comment_id, text, problem,
                        api_key=credentials.get("anthropic_api_key", ""),
                    )
                else:
                    outcome = decisions_call(
                        comment_id, text, problem,
                        api_key=credentials.get("openai_api_key", ""), model=config.luna_model,
                    )
            except Exception as exc:
                outcome = exc
        if isinstance(outcome, Judgement) and not outcome.error:
            return Combined(
                None, None, outcome.kind or "", outcome.answer, outcome.bare_term,
                method, None, **{method: outcome},
            )
        logged = outcome if isinstance(outcome, Judgement) else Judgement(
            method, None, error=str(outcome), debug=getattr(outcome, "debug", {}),
        )
        fallback = call_luna()
        if isinstance(fallback, Exception):
            raise fallback
        if not isinstance(fallback, Judgement):
            raise RuntimeError("Luna returned no judgement")
        if fallback.error:
            raise RuntimeError(fallback.error)
        return Combined(
            fallback, None, fallback.kind or "", fallback.answer, fallback.bare_term,
            f"{method}_fallback_luna", None, [f"{method}: {logged.error}"],
            **{method: logged},
        )

    if need_luna and need_jev and not supplied:
        with ThreadPoolExecutor(max_workers=2) as executor:
            luna_future = executor.submit(call_luna)
            jev_future = executor.submit(call_jev)
            luna_outcome = luna_future.result()
            jev_outcome = jev_future.result()
    else:
        luna_outcome = call_luna() if need_luna else None
        jev_outcome = call_jev() if need_jev else None

    jev_failed = isinstance(jev_outcome, Exception) or (
        isinstance(jev_outcome, Judgement) and bool(jev_outcome.error)
    )
    if config.judge_mode == "jev" and jev_failed:
        luna_outcome = call_luna()
    if isinstance(luna_outcome, Exception) and (need_luna or isinstance(jev_outcome, Exception)):
        raise luna_outcome
    if config.judge_mode == "luna" and not isinstance(luna_outcome, Judgement):
        raise RuntimeError("Luna returned no judgement")

    errors: list[str] = []
    if isinstance(jev_outcome, Exception):
        errors.append(f"jev: {jev_outcome}")
    luna_result = luna_outcome if isinstance(luna_outcome, Judgement) else None
    jev_result = jev_outcome if isinstance(jev_outcome, Judgement) else None
    jev_logged = (
        Judgement("jev", None, error=str(jev_outcome))
        if isinstance(jev_outcome, Exception) else jev_result
    )
    if luna_result is not None and luna_result.error:
        raise RuntimeError(luna_result.error)
    if jev_result is not None and jev_result.error:
        errors.append(f"jev: {jev_result.error}")
        jev_result = None

    if config.judge_mode == "jev":
        if jev_result is not None:
            chosen, decision = jev_result, "jev"
        elif luna_result is not None:
            chosen, decision = luna_result, "jev_fallback_luna"
        else:
            raise RuntimeError("both judges failed")
    else:
        if luna_result is None:
            raise RuntimeError("Luna returned no judgement")
        chosen, decision = luna_result, "luna"

    mismatch = None
    if luna_result is not None and jev_result is not None:
        mismatch = (luna_result.kind, luna_result.answer) != (jev_result.kind, jev_result.answer)
        if config.judge_mode == "hybrid" and config.shadow and mismatch:
            LOGGER.warning("JUDGE_SHADOW_MISMATCH %s", json.dumps({
                "comment_id": comment_id, "media_id": media_id or problem.media_id,
                "luna": {"kind": luna_result.kind, "answer": luna_result.answer},
                "jev": {"kind": jev_result.kind, "answer": jev_result.answer},
            }, ensure_ascii=False, separators=(",", ":")))

    if config.judge_mode == "hybrid" and config.consensus and chosen.kind == "guess_correct":
        if jev_result is not None and jev_result.kind == "guess_correct":
            decision = "consensus_ok"
        else:
            decision = "consensus_split"
            LOGGER.warning("JUDGE_CONSENSUS_SPLIT %s", json.dumps({
                "comment_id": comment_id, "media_id": media_id or problem.media_id,
                "luna_kind": chosen.kind,
                "jev_kind": jev_result.kind if jev_result else None,
            }, ensure_ascii=False, separators=(",", ":")))
    return Combined(
        luna_result, jev_logged, chosen.kind or "", chosen.answer,
        chosen.bare_term, decision, mismatch, errors,
    )
