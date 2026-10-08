"""Offline regression checks for the migrated trial classifiers."""

from __future__ import annotations

import io
import json
import logging
from dataclasses import replace
from unittest.mock import Mock
from urllib.error import HTTPError

import pytest

from app import http_util
from app.config import Config
from app.judge import jev, luna
from app.judge.combiner import combine
from app.judge.contract import JudgeCriteria, Judgement, Problem, ProblemInvalid


class _Response:
    def __init__(self, value: dict) -> None:
        self.body = json.dumps(value, ensure_ascii=False).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self) -> bytes:
        return self.body


def _snapshot(problem) -> dict:
    return {
        **problem.__dict__,
        "fact_sheet": list(problem.fact_sheet),
        "core_points": list(problem.core_points),
        "judge_criteria": {
            "points": [{"hit": hit, "touch": touch}
                       for hit, touch in problem.judge_criteria.points],
            "errors": list(problem.judge_criteria.errors),
        },
    }


def test_problem_requires_v3_and_judge_criteria(problem) -> None:
    raw = _snapshot(problem)
    assert Problem.from_snapshot(raw) == problem
    with pytest.raises(ProblemInvalid, match="schema_version"):
        Problem.from_snapshot({**raw, "schema_version": 2})
    with pytest.raises(ProblemInvalid, match="core_points"):
        Problem.from_snapshot({**raw, "core_points": []})
    with pytest.raises(ProblemInvalid, match="reveal_text"):
        Problem.from_snapshot({**raw, "reveal_text": None})
    assert isinstance(problem.judge_criteria.points, tuple)
    assert isinstance(problem.judge_criteria.errors, tuple)


@pytest.mark.parametrize("criteria", [
    None,
    {"points": [], "errors": []},
    {"points": [{"hit": "当てた", "touch": "触れた"}], "errors": []},
    {"points": [{"hit": "", "touch": "触れた"}] * 2, "errors": []},
    {"points": [{"hit": "当てた", "touch": 1}] * 2, "errors": []},
    {"points": [{"hit": "当てた", "touch": "触れた"}] * 2,
     "errors": ["a", "b", "c", "d"]},
    {"points": [{"hit": "当てた", "touch": "触れた"}] * 2,
     "errors": [" "]},
])
def test_problem_rejects_invalid_judge_criteria(problem, criteria) -> None:
    with pytest.raises(ProblemInvalid, match="judge_criteria"):
        Problem.from_snapshot({**_snapshot(problem), "judge_criteria": criteria})


def test_luna_formats_judge_criteria(problem) -> None:
    lines = luna.format_judge_criteria(problem).splitlines()
    for index, (point, (hit, touch)) in enumerate(
        zip(problem.core_points, problem.judge_criteria.points), start=1
    ):
        assert lines[(index - 1) * 3:(index - 1) * 3 + 3] == [
            f"- 要点 {index}: {point}", f"  当てた: {hit}", f"  触れた: {touch}",
        ]
    assert lines[-1] == "- 正解にしない誤りの例: " + "／".join(problem.judge_criteria.errors)
    no_errors = replace(problem, judge_criteria=JudgeCriteria(
        problem.judge_criteria.points, ()
    ))
    assert luna.format_judge_criteria(no_errors).splitlines()[-1] == (
        "- 正解にしない誤りの例: なし"
    )


def test_luna_parses_strict_json_and_retries_429(monkeypatch, tmp_path, problem) -> None:
    decision = {"kind": "q_open", "answer": None, "reply": "聞き直してね",
                "reason": "語だけ", "bare_term": "レントゲン"}
    body = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(decision)}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20,
                      "completion_tokens_details": {"reasoning_tokens": 7}}}
    calls = []

    def open_request(req, timeout):
        calls.append(json.loads(req.data))
        if len(calls) == 1:
            raise HTTPError(req.full_url, 429, "rate", {}, io.BytesIO(b""))
        return _Response(body)

    monkeypatch.setattr(http_util.request, "urlopen", open_request)
    rules = tmp_path / "rules.txt"
    rules.write_text("{judge_criteria}", encoding="utf-8")
    monkeypatch.setattr(luna, "RULES_PATH", rules)
    sleep = Mock()
    monkeypatch.setattr(http_util.time, "sleep", sleep)
    result = luna.judge("1", "レントゲン？", problem, api_key="fake")
    assert (result.kind, result.bare_term, result.reason) == ("q_open", "レントゲン", "語だけ")
    assert result.debug["reasoning_tokens"] == 7
    assert len(calls) == 2
    assert "temperature" not in calls[0]
    assert calls[0]["reasoning_effort"] == "xhigh"
    assert calls[0]["max_completion_tokens"] == 2400
    assert calls[0]["messages"][0]["content"] == luna.format_judge_criteria(problem)
    schema = calls[0]["response_format"]["json_schema"]
    assert schema["strict"] is True
    assert "bare_term" in schema["schema"]["required"]
    assert sleep.call_args.args == (5,)


def test_luna_normalizes_bare_term_and_prevents_correct_disclosure(monkeypatch, problem) -> None:
    body = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps({
        "kind": "guess_correct", "answer": None, "reply": "正解！", "reason": "語だけ",
        "bare_term": "別の表記",
    })}}]}
    monkeypatch.setattr(luna, "post_json_with_retry", lambda *args, **kwargs: body)
    result = luna.judge("1", "【レントゲン？】", problem, api_key="fake")
    assert result.kind == "q_open"
    assert result.bare_term == "レントゲン"


def test_jev_stage_zero_and_bare_term_precede_core(monkeypatch, problem) -> None:
    api = Mock(side_effect=AssertionError("API must not be called"))
    monkeypatch.setattr(jev, "_record_call", api)
    assert jev.judge("1", "https://example.com", problem, api_key="fake").kind == "spam"
    assert jev.judge("1", "nice puzzle", problem, api_key="fake").kind == "foreign"
    assert jev.judge("1", "！", problem, api_key="fake").kind == "emoji_only"
    api.assert_not_called()

    questions = []

    def bare(*args):
        questions.append(args[2])
        return {
            "major": {"choice": "question_or_guess"},
            "bare_term": {"noul": {"true": 0.9}},
        }

    monkeypatch.setattr(jev, "_record_call", bare)
    result = jev.judge("1", "レントゲン？", problem, api_key="fake")
    assert (result.kind, result.bare_term) == ("q_open", "レントゲン")
    assert result.debug["probabilities"]["A_bare"] == 0.9
    assert len(questions) == 1
    assert set(questions[0]) == {"major", "bare_term"}


def test_jev_bare_term_only_applies_to_question_or_guess(monkeypatch, problem) -> None:
    calls = []

    def record_call(api_key, state, questions, debug):
        calls.append(questions)
        if "major" in questions:
            return {
                "major": {"choice": "reaction"},
                "bare_term": {"noul": {"true": 0.95}},
            }
        if "kind" in questions:
            return {"kind": {"choice": "impression"}}
        raise AssertionError(f"unexpected stage: {questions.keys()}")

    monkeypatch.setattr(jev, "_record_call", record_call)
    result = jev.judge("1", "天才", problem, api_key="fake")
    assert result.kind == "impression"
    assert result.bare_term is None
    assert len(calls) == 2


def test_jev_correct_requires_every_core_point(monkeypatch, problem) -> None:
    def run_with(second: float, contradiction: float = 0.1) -> Judgement:
        def call(api_key, state, questions, debug):
            name = next(iter(questions))
            if name == "major":
                return {
                    "major": {"choice": "question_or_guess"},
                    "bare_term": {"noul": {"true": 0.1}},
                }
            if name == "qg":
                return {name: {"probabilities": {"guess": 0.99, "question": 0.01}}}
            if name == "point_0":
                assert all(question["type"] == "choice" for question in questions.values())
                assert set(questions["point_0"]["criteria"]) == {"hit", "touch", "none"}
                assert problem.core_points[0] in questions["point_0"]["criteria"]["hit"]
                assert problem.judge_criteria.points[0][0] in questions["point_0"]["criteria"]["hit"]
                assert problem.judge_criteria.points[0][1] in questions["point_0"]["criteria"]["touch"]
                # 21-6d16: 誤りでない部分だけで数えるため、段 B にも真相と確定事実を渡す
                assert state["truth"] == problem.truth and state["fact_sheet"] == list(problem.fact_sheet)
                return {"point_0": {"probabilities": {"hit": 0.8, "touch": 0.1, "none": 0.1}},
                        "point_1": {"probabilities": {"hit": second, "touch": 0.3,
                                                      "none": 0.7 - second}}}
            if name == "contradict":
                assert {"truth", "fact_sheet", "comment", "errors"} <= set(state)
                assert state["errors"] == list(problem.judge_criteria.errors)
                return {"contradict": {"noul": {"true": contradiction}}}
            raise AssertionError(name)

        monkeypatch.setattr(jev, "_record_call", call)
        return jev.judge("1", "男はレントゲンで回復を知った", problem, api_key="fake")

    close = run_with(0.49)
    assert close.kind == "guess_close"
    assert close.debug["probabilities"]["B"]["point_1"] == {"hit": 0.49, "close": 0.79}
    assert run_with(0.5).kind == "guess_correct"


def test_jev_touch_can_be_close_without_hit(monkeypatch, problem) -> None:
    def call(api_key, state, questions, debug):
        name = next(iter(questions))
        if name == "major":
            return {"major": {"choice": "question_or_guess"},
                    "bare_term": {"noul": {"true": 0.1}}}
        if name == "qg":
            return {"qg": {"probabilities": {"guess": 0.99, "question": 0.01}}}
        if name == "point_0":
            return {"point_0": {"probabilities": {"hit": 0.1, "touch": 0.3, "none": 0.6}},
                    "point_1": {"choice": "none"}}
        raise AssertionError(name)

    monkeypatch.setattr(jev, "_record_call", call)
    result = jev.judge("1", "影は体内のこと？", problem, api_key="fake")
    assert result.kind == "guess_close"
    assert result.debug["probabilities"]["B"] == {
        "point_0": {"hit": 0.1, "close": 0.4},
        "point_1": {"hit": 0.0, "close": 0.0},
    }


@pytest.mark.parametrize("choice, expected", [
    ("hit", {"hit": 1.0, "close": 1.0}),
    ("touch", {"hit": 0.0, "close": 1.0}),
    ("none", {"hit": 0.0, "close": 0.0}),
])
def test_jev_core_choice_only_is_one_hot(choice, expected) -> None:
    assert jev._core_point_probabilities({"choice": {"key": choice}}) == expected


def test_jev_contradiction_demotes_correct_candidate(monkeypatch, problem) -> None:
    def run_with(second: float, contradiction: float) -> tuple[Judgement, list[str]]:
        names = []

        def call(api_key, state, questions, debug):
            name = next(iter(questions))
            names.append(name)
            if name == "major":
                return {
                    "major": {"choice": "question_or_guess"},
                    "bare_term": {"noul": {"true": 0.1}},
                }
            if name == "qg":
                return {name: {"probabilities": {"guess": 0.99, "question": 0.01}}}
            if name == "point_0":
                return {"point_0": {"probabilities": {"hit": 0.9, "touch": 0.05, "none": 0.05}},
                        "point_1": {"probabilities": {"hit": second, "touch": 0.2,
                                                      "none": 0.8 - second}}}
            if name == "contradict":
                return {"contradict": {"noul": {"true": contradiction}}}
            raise AssertionError(name)

        monkeypatch.setattr(jev, "_record_call", call)
        result = jev.judge("1", "男はレントゲンで回復を知った", problem, api_key="fake",
                           t_contradict=0.5)
        return result, names

    result, names = run_with(0.9, 0.5)
    assert result.kind == "guess_close"
    assert result.debug["probabilities"]["B2"] == 0.5
    assert "矛盾=0.50" in result.reason
    assert names.count("contradict") == 1
    result, _ = run_with(0.9, 0.49)
    assert result.kind == "guess_correct"
    # ④ の候補でなければ矛盾チェックは呼ばない
    result, names = run_with(0.3, 0.9)
    assert result.kind == "guess_close"
    assert "contradict" not in names
    assert "B2" not in result.debug["probabilities"]


def test_jev_low_confidence_answer_falls_back_to_irrelevant(monkeypatch, problem) -> None:
    def run_with(probabilities: dict) -> Judgement:
        def call(api_key, state, questions, debug):
            name = next(iter(questions))
            if name == "major":
                return {
                    "major": {"choice": "question_or_guess"},
                    "bare_term": {"noul": {"true": 0.1}},
                }
            if name == "qg":
                return {name: {"probabilities": {"guess": 0.01, "question": 0.99}}}
            if name == "kind":
                return {name: {"choice": "q_yesno"}}
            if name == "point_0":
                return {"point_0": {"probabilities": {"hit": 0.1, "touch": 0.1, "none": 0.8}},
                        "point_1": {"probabilities": {"hit": 0.1, "touch": 0.1, "none": 0.8}}}
            if name == "quality":
                return {name: {"noul": {"true": 0.99}}}
            if name == "answer":
                return {name: {"probabilities": probabilities}}
            raise AssertionError(name)

        monkeypatch.setattr(jev, "_record_call", call)
        return jev.judge("1", "男は病院にいた？", problem, api_key="fake")

    result = run_with({"yes": 0.5, "no": 0.4, "irrelevant": 0.1})
    assert (result.kind, result.answer) == ("q_yesno", "irrelevant")
    result = run_with({"yes": 0.1, "no": 0.8, "irrelevant": 0.1})
    assert (result.kind, result.answer) == ("q_yesno", "no")


def _j(method: str, kind: str, answer: str | None = None) -> Judgement:
    return Judgement(method, kind, answer=answer, reason="stub")


@pytest.mark.parametrize("mode", ["luna", "jev", "hybrid"])
def test_combiner_three_modes(mode, problem) -> None:
    luna_call = Mock(return_value=_j("luna", "q_yesno", "yes"))
    jev_call = Mock(return_value=_j("jev", "q_yesno", "yes"))
    result = combine("c", "q", problem, Config(judge_mode=mode), {},
                     luna_call=luna_call, jev_call=jev_call)
    assert result.kind == "q_yesno"
    assert result.decision == ("jev" if mode == "jev" else "luna")
    assert luna_call.call_count == (0 if mode == "jev" else 1)
    assert jev_call.call_count == (0 if mode == "luna" else 1)


def test_combiner_shadow_and_consensus_cases(caplog, problem) -> None:
    config = Config(judge_mode="hybrid")
    correct = _j("luna", "guess_correct")
    jev_correct = _j("jev", "guess_correct")
    jev_close = _j("jev", "guess_close")
    with caplog.at_level(logging.WARNING):
        same = combine("c", "text", problem, config, {},
                       precomputed={"luna": correct, "jev": jev_correct})
        split = combine("d", "text", problem, config, {},
                        precomputed={"luna": correct, "jev": jev_close})
        failed = combine("e", "text", problem, config, {},
                         precomputed={"luna": correct, "jev": RuntimeError("jev down")})
        only_jev_correct = combine("f", "text", problem, config, {},
                                   precomputed={"luna": _j("luna", "guess_close"), "jev": jev_correct})
    assert same.decision == "consensus_ok" and same.mismatch is False
    assert split.decision == "consensus_split" and split.mismatch is True
    assert failed.decision == "consensus_split" and failed.jev.error == "jev down"
    assert "jev down" in failed.errors[0]
    assert only_jev_correct.decision == "luna"
    assert caplog.text.count("JUDGE_CONSENSUS_SPLIT") == 2
    assert "JUDGE_SHADOW_MISMATCH" in caplog.text


def test_combiner_independent_switches_and_jev_fallback(problem, caplog) -> None:
    correct = _j("luna", "guess_correct")
    close = _j("jev", "guess_close")
    with caplog.at_level(logging.WARNING):
        no_shadow = combine("c", "text", problem, Config(shadow=False, consensus=True), {},
                            precomputed={"luna": correct, "jev": close})
        no_consensus = combine("c", "text", problem, Config(shadow=True, consensus=False), {},
                               precomputed={"luna": correct, "jev": close})
        both_off = combine("c", "text", problem, Config(shadow=False, consensus=False), {},
                           luna_call=lambda *args, **kwargs: correct,
                           jev_call=lambda *args, **kwargs: pytest.fail("Jev should not run"))
    assert no_shadow.decision == "consensus_split"
    assert no_consensus.decision == "luna"
    assert both_off.jev is None and both_off.decision == "luna"
    assert caplog.text.count("JUDGE_SHADOW_MISMATCH") == 1

    fallback = combine("c", "text", problem, Config(judge_mode="jev"), {},
                       precomputed={"jev": RuntimeError("down"), "luna": correct})
    assert fallback.decision == "jev_fallback_luna"
    assert fallback.kind == "guess_correct"
    error_result = combine("c", "text", problem, Config(judge_mode="jev"), {},
                           precomputed={"jev": Judgement("jev", None, error="bad response"),
                                        "luna": correct})
    assert error_result.decision == "jev_fallback_luna"
    assert error_result.jev.error == "bad response"
    with pytest.raises(RuntimeError, match="luna down"):
        combine("c", "text", problem, Config(judge_mode="luna"), {},
                precomputed={"luna": RuntimeError("luna down")})
