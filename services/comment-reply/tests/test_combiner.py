"""Three-mode judging, sequential fallbacks, error records and configuration."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from app.comment_log import apply_decision, new_record
from app.config import Config, HAIKU_EFFORTS, JUDGE_MODES, LUNA_EFFORTS, REPLY_VARIANTS
from app.judge.combiner import combine
from app.judge.contract import Judgement
from app.reply.writer import Reply


FALLBACKS = {"haiku": "luna", "luna": "haiku", "jev": "haiku"}
CREDENTIALS = {"openai_api_key": "openai", "typesafe_api_key": "jev", "anthropic_api_key": "anthropic"}


def _calls(outcomes: dict, order: list[str]) -> dict:
    def call(method: str):
        def run(*args, **kwargs):
            order.append(method)
            outcome = outcomes[method]
            if isinstance(outcome, Exception):
                raise outcome
            return outcome
        return Mock(side_effect=run)
    return {f"{method}_call": call(method) for method in FALLBACKS}


def _failure(method: str, form: str):
    debug = {"calls": 1, "input_tokens": 23}
    if form == "exception":
        error = ValueError(f"{method} down")
        error.debug = debug
        return error
    return Judgement(method, None, error=f"{method} down", debug=debug)


@pytest.mark.parametrize("mode", FALLBACKS)
def test_main_success_calls_only_main(mode, problem) -> None:
    order = []
    success = Judgement(mode, "q_yesno", "yes")
    calls = _calls({mode: success}, order)
    result = combine("c", "質問", problem, Config(judge_mode=mode), CREDENTIALS, **calls)
    assert order == [mode]
    assert result.decision == mode and result.kind == "q_yesno" and result.answer == "yes"
    assert result.errors == []
    assert getattr(result, mode) is success
    for other in FALLBACKS.keys() - {mode}:
        assert getattr(result, other) is None
        calls[f"{other}_call"].assert_not_called()


@pytest.mark.parametrize("mode,fallback", FALLBACKS.items())
@pytest.mark.parametrize("form", ["exception", "error"])
def test_main_failure_calls_fallback_and_records_both(mode, fallback, form, problem) -> None:
    order = []
    success = Judgement(fallback, "q_open", bare_term="レントゲン")
    calls = _calls({mode: _failure(mode, form), fallback: success}, order)
    config = Config(judge_mode=mode, luna_effort="medium", haiku_effort="max")
    result = combine("c", "レントゲン？", problem, config, CREDENTIALS, **calls)
    assert order == [mode, fallback]
    assert (result.kind, result.answer, result.bare_term) == ("q_open", None, "レントゲン")
    assert result.decision == f"{mode}_fallback_{fallback}"
    assert result.errors == [f"{mode}: {mode} down"]
    assert getattr(result, mode).error == f"{mode} down"
    assert getattr(result, mode).debug == {"calls": 1, "input_tokens": 23}
    assert getattr(result, fallback) is success
    expected = {
        "luna": {"api_key": "openai", "model": "gpt-6-luna", "effort": "medium"},
        "haiku": {"api_key": "anthropic", "effort": "max"},
        "jev": {"api_key": "jev"},
    }
    for method in (mode, fallback):
        calls[f"{method}_call"].assert_called_once_with("c", "レントゲン？", problem, **expected[method])
    record = new_record({"id": "c", "text": "レントゲン？"}, None, "now", config, problem)
    apply_decision(record, result, Reply("何がレントゲン？", "template", False))
    assert record["final"]["decision"] == result.decision
    assert record["errors"] == result.errors
    assert record["judgements"][mode]["error"] == f"{mode} down"
    assert record["judgements"][fallback]["kind"] == "q_open"


@pytest.mark.parametrize("mode,fallback", FALLBACKS.items())
@pytest.mark.parametrize("main_form", ["exception", "error"])
@pytest.mark.parametrize("fallback_form", ["exception", "error"])
def test_both_fail_raise_without_a_third_judge(mode, fallback, main_form, fallback_form, problem) -> None:
    order = []
    calls = _calls({mode: _failure(mode, main_form), fallback: _failure(fallback, fallback_form)}, order)
    with pytest.raises(RuntimeError, match="both judges failed") as caught:
        combine("c", "質問", problem, Config(judge_mode=mode), CREDENTIALS, **calls)
    assert order == [mode, fallback]
    assert f"{mode} down" in str(caught.value) and f"{fallback} down" in str(caught.value)
    for other in FALLBACKS.keys() - {mode, fallback}:
        calls[f"{other}_call"].assert_not_called()


@pytest.mark.parametrize("mode,fallback", FALLBACKS.items())
def test_precomputed_failure_uses_the_same_fallback(mode, fallback, problem) -> None:
    blocked = Mock(side_effect=AssertionError("all required judgements are supplied"))
    result = combine("c", "質問", problem, Config(judge_mode=mode), {},
                     precomputed={mode: _failure(mode, "error"), fallback: Judgement(fallback, "impression")},
                     luna_call=blocked, jev_call=blocked, haiku_call=blocked)
    assert result.decision == f"{mode}_fallback_{fallback}"
    blocked.assert_not_called()


def test_config_defaults_and_independent_writer_variants() -> None:
    assert Config.from_env({}) == Config()
    config = Config()
    assert (config.judge_mode, config.reply_variant, config.haiku_effort, config.luna_effort) == (
        "haiku", "1b-haiku", "high", "xhigh",
    )
    assert JUDGE_MODES == {"luna", "jev", "haiku"}
    assert REPLY_VARIANTS == {"1b", "1d-luna", "2b", "2c-luna", "1b-haiku", "1d-haiku"}
    assert LUNA_EFFORTS == HAIKU_EFFORTS == {"low", "medium", "high", "xhigh", "max"}
    for mode in JUDGE_MODES:
        for variant in REPLY_VARIANTS:
            assert Config.from_env({"JUDGE_MODE": mode, "REPLY_VARIANT": variant}).reply_variant == variant
    assert Config.from_env({"JUDGE_SHADOW": "unused", "JUDGE_CONSENSUS": "unused"}) == Config()


@pytest.mark.parametrize("mode", ["hybrid", "decisions", "invalid"])
def test_config_rejects_removed_modes(mode) -> None:
    with pytest.raises(ValueError, match="JUDGE_MODE"):
        Config.from_env({"JUDGE_MODE": mode})


@pytest.mark.parametrize("effort", ["low", "medium", "high", "xhigh", "max"])
def test_config_luna_effort(effort) -> None:
    assert Config.from_env({"LUNA_EFFORT": effort}).luna_effort == effort


@pytest.mark.parametrize("effort", ["", "invalid", "MAX", " high", "off"])
def test_config_rejects_invalid_luna_effort(effort) -> None:
    with pytest.raises(ValueError, match="LUNA_EFFORT"):
        Config.from_env({"LUNA_EFFORT": effort})
