"""Offline Decisions transport, shared-stage and fallback regression checks."""

from __future__ import annotations

import io
import json
from copy import deepcopy
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

import pytest

from app import http_util
from app.comment_log import apply_decision, new_record
from app.config import Config
from app.judge import decisions, jev
from app.judge.combiner import combine
from app.judge.contract import Judgement
from app.reply.writer import Reply
from tools import local_trial


class _Response:
    def __init__(self, body) -> None:
        self.body = json.dumps(body, ensure_ascii=False).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self) -> bytes:
        return self.body


QUESTIONS = {
    "major": {"type": "choice", "instructions": "Shared classification instructions.",
              "criteria": {"first": "最初の説明", "second": "次の説明"}},
    "bare_term": {"type": "noul", "instructions": "Shared predicate instructions.",
                  "criteria": {"true": "bare", "false": "sentence"}},
}
BODY = {
    "model": "gpt-6-luna",
    "answers": [
        {"type": "choice", "name": "major", "choice": "second", "confidence": 0.01,
         "probabilities": [{"value": "first", "probability": .3},
                           {"value": "second", "probability": .7}]},
        {"type": "predicate", "name": "bare_term", "probability": .8},
    ],
    "usage": {"input_tokens": 42, "output_tokens": 0},
}


def test_request_translation_and_response_jev_parsers(monkeypatch) -> None:
    state = {"context": "文脈", "comment": "語句？", "facts": ("事実",)}
    requests = []

    def open_request(req, timeout):
        requests.append(req)
        return _Response(BODY)

    monkeypatch.setattr(http_util.request, "urlopen", open_request)
    result = decisions._decisions_request("fake-key", state, QUESTIONS)
    req = requests[0]
    payload = json.loads(req.data)
    assert req.full_url == "https://api.openai.com/v1/decisions"
    assert req.get_method() == "POST"
    assert req.get_header("Authorization") == "Bearer fake-key"
    assert req.get_header("Content-type") == "application/json"
    assert payload == {
        "model": "gpt-6-luna", "input": json.dumps(state, ensure_ascii=False),
        "questions": [
            {"type": "choice", "name": "major", "instructions": QUESTIONS["major"]["instructions"],
             "choices": [{"value": "first", "description": "最初の説明"},
                         {"value": "second", "description": "次の説明"}]},
            {"type": "predicate", "name": "bare_term",
             "instructions": QUESTIONS["bare_term"]["instructions"]
             + "\nTrue: bare\nFalse: sentence"},
        ],
    }
    assert "語句？" in payload["input"]
    assert list(result["answers"]) == ["major", "bare_term"]
    assert jev._noul_true(result["answers"]["bare_term"]) == .8
    assert jev._choice(result["answers"]["major"], ("first", "second")) == "second"
    assert jev._probability_map(result["answers"]["major"]) == {"first": .3, "second": .7}
    assert result["confidence"] == {"major": .01}
    assert result["refusals"] == {"count": 0, "names": []}


@pytest.mark.parametrize("status", [429, 500, 503, 529, 599])
def test_retry_three_times_with_exponential_backoff(monkeypatch, status) -> None:
    calls = []

    def open_request(req, timeout):
        calls.append(req)
        if len(calls) <= 3:
            raise HTTPError(req.full_url, status, "retry", {}, io.BytesIO(b""))
        return _Response(BODY)

    monkeypatch.setattr(http_util.request, "urlopen", open_request)
    sleep = Mock()
    monkeypatch.setattr(http_util.time, "sleep", sleep)
    result = decisions._decisions_request("fake", {"comment": "語"}, QUESTIONS)
    assert result["usage"] == BODY["usage"]
    assert len(calls) == 4
    assert [call.args for call in sleep.call_args_list] == [(1,), (2,), (4,)]
    assert all(req.data == calls[0].data for req in calls)


@pytest.mark.parametrize("status, attempts", [(429, 4), (503, 4), (401, 1)])
def test_http_failure_raises_after_retry_budget(monkeypatch, status, attempts) -> None:
    api = Mock(side_effect=HTTPError(decisions.DECISIONS_URL, status, "failed", {}, None))
    monkeypatch.setattr(http_util.request, "urlopen", api)
    monkeypatch.setattr(http_util.time, "sleep", Mock())
    with pytest.raises(decisions.DecisionsError, match=f"HTTP {status}"):
        decisions._decisions_request("fake", {}, QUESTIONS)
    assert api.call_count == attempts


@pytest.mark.parametrize("body", [[], "invalid", None])
def test_non_object_http_response_raises(monkeypatch, body) -> None:
    monkeypatch.setattr(http_util.request, "urlopen", lambda *args, **kwargs: _Response(body))
    with pytest.raises(decisions.DecisionsError, match="応答を読めません"):
        decisions._decisions_request("fake", {}, QUESTIONS)


def test_network_or_invalid_json_failure_is_decisions_error(monkeypatch) -> None:
    for failure in (URLError("offline"), json.JSONDecodeError("invalid", "", 0)):
        monkeypatch.setattr(decisions, "post_json_with_retry", Mock(side_effect=failure))
        with pytest.raises(decisions.DecisionsError, match="応答を読めません"):
            decisions._decisions_request("fake", {}, QUESTIONS)


@pytest.mark.parametrize("field, value", [
    ("model", None), ("usage", None), ("answers", {}), ("answers", []),
    ("input_tokens", -1), ("output_tokens", True),
    ("name", "unexpected"), ("type", "score"),
    ("probability", -0.1), ("probability", 1.1), ("probability", "0.5"),
    ("probability", True), ("probability", float("nan")),
    ("choice", "missing"), ("confidence", None),
    ("probabilities", []),
    ("probabilities", [{"value": "first", "probability": .5}] * 2),
    ("probabilities", [{"value": "first", "probability": .2},
                       {"value": "other", "probability": .8}]),
    ("probabilities", [{"value": "first", "probability": .1},
                       {"value": "second", "probability": .1}]),
])
def test_malformed_scored_responses_raise(field, value) -> None:
    body = deepcopy(BODY)
    if field in {"model", "usage", "answers"}:
        body[field] = value
    elif field in {"input_tokens", "output_tokens"}:
        body["usage"][field] = value
    elif field == "probability":
        body["answers"][1][field] = value
    else:
        body["answers"][0][field] = value
    with pytest.raises(decisions.DecisionsError, match="形が不正"):
        decisions._convert_response(body, QUESTIONS)


def test_answer_order_and_missing_fields_are_errors() -> None:
    body = deepcopy(BODY)
    body["answers"].reverse()
    with pytest.raises(decisions.DecisionsError, match="out-of-order"):
        decisions._convert_response(body, QUESTIONS)
    for field in ("model", "usage", "answers"):
        body = deepcopy(BODY)
        del body[field]
        with pytest.raises(decisions.DecisionsError):
            decisions._convert_response(body, QUESTIONS)


def test_refusal_raises_and_keeps_stage_telemetry(monkeypatch, problem) -> None:
    def open_request(req, timeout):
        questions = json.loads(req.data)["questions"]
        return _Response({
            "model": decisions.MODEL,
            "answers": [{"type": "refusal", "name": q["name"]} for q in questions],
            "usage": {"input_tokens": 42, "output_tokens": 0},
        })

    monkeypatch.setattr(http_util.request, "urlopen", open_request)
    with pytest.raises(decisions.DecisionsError, match="refusal") as caught:
        decisions.judge("c", "質問", problem, api_key="fake")
    debug = caught.value.debug
    assert debug["calls"] == 1 and debug["input_tokens"] == 42
    assert debug["output_tokens"] == 0 and debug["latency_s"] >= 0
    assert debug["refusals"] == {"count": 2, "names": ["major", "bare_term"]}
    assert debug["confidence"] == {"A1": {}}


def test_partial_refusal_keeps_other_question_confidence(monkeypatch) -> None:
    body = deepcopy(BODY)
    body["answers"][1] = {"type": "refusal", "name": "bare_term"}
    monkeypatch.setattr(http_util.request, "urlopen", lambda *args, **kwargs: _Response(body))
    with pytest.raises(decisions.DecisionsError) as caught:
        decisions._decisions_request("fake", {}, QUESTIONS)
    assert caught.value.debug["confidence"] == {"major": .01}
    assert caught.value.debug["refusals"] == {"count": 1, "names": ["bare_term"]}


def _scripted_transport(monkeypatch, overrides: dict):
    values = {
        "major": "question_or_guess", "bare_term": .1,
        "qg": {"question": .99, "guess": .01}, "kind": "q_yesno",
        "point_0": {"hit": .1, "touch": .1, "none": .8},
        "point_1": {"hit": .1, "touch": .1, "none": .8},
        "recheck": .9, "contradict": .1, "quality": .99,
        "answer": {"yes": .1, "no": .8, "irrelevant": .1},
        **overrides,
    }
    payloads = {"jev": [], "decisions": []}

    def open_request(req, timeout):
        payload = json.loads(req.data)
        is_decisions = req.full_url == decisions.DECISIONS_URL
        method = "decisions" if is_decisions else "jev"
        payloads[method].append(payload)
        answers = {}
        for name, question in ([(q["name"], q) for q in payload["questions"]]
                               if is_decisions else payload["questions"].items()):
            value = values[name]
            if question["type"] in {"predicate", "noul"}:
                answer = ({"type": "predicate", "name": name, "probability": value}
                          if is_decisions else {"noul": {"true": value}})
            else:
                keys = ([entry["value"] for entry in question["choices"]]
                        if is_decisions else list(question["criteria"]))
                probabilities = value if isinstance(value, dict) else {
                    key: float(key == value) for key in keys
                }
                chosen = max(probabilities, key=probabilities.get)
                answer = {"choice": chosen, "probabilities": probabilities}
                if is_decisions:
                    answer = {**answer, "type": "choice", "name": name, "confidence": .01,
                              "probabilities": [{"value": key, "probability": probability}
                                                for key, probability in probabilities.items()]}
            answers[name] = answer
        return _Response({
            "model": payload["model"],
            "answers": list(answers.values()) if is_decisions else answers,
            "usage": {"input_tokens": 10, "output_tokens": 2},
        })

    monkeypatch.setattr(http_util.request, "urlopen", open_request)
    monkeypatch.setattr(jev.time, "monotonic", lambda: 0.0)
    return payloads


@pytest.mark.parametrize("text, overrides, kind, answer, stages", [
    ("https://example.com", {}, "spam", None, []),
    ("！", {}, "emoji_only", None, []),
    ("nice puzzle", {}, "foreign", None, []),
    ("レントゲン？", {"bare_term": .9}, "q_open", None, ["major"]),
    ("感想", {"major": "reaction", "bare_term": .9, "kind": "impression"},
     "impression", None, ["major", "kind"]),
    ("ヒント", {"major": "request", "kind": "ask_hint"},
     "ask_hint", None, ["major", "kind"]),
    ("不適切", {"major": "inappropriate", "kind": "abuse"},
     "abuse", None, ["major", "kind"]),
    ("其他", {"major": "other"}, "foreign", None, ["major"]),
    ("複数質問", {"kind": "q_multi"}, "q_multi", None, ["major", "qg", "kind"]),
    ("なぜ？", {"kind": "q_open", "recheck": .2}, "q_open", None,
     ["major", "qg", "kind", "recheck"]),
    ("男は病院にいた？", {}, "q_yesno", "no",
     ["major", "qg", "kind", "point_0", "quality", "answer"]),
    ("その人は病院にいた？", {}, "q_yesno", "no",
     ["major", "qg", "kind", "recheck", "point_0", "quality", "answer"]),
    ("質問", {"quality": .1}, "q_open", None,
     ["major", "qg", "kind", "point_0", "quality"]),
    ("質問", {"answer": {"yes": .5, "no": .4, "irrelevant": .1}}, "q_yesno", "irrelevant",
     ["major", "qg", "kind", "point_0", "quality", "answer"]),
    ("推理", {"qg": {"question": .01, "guess": .99},
              "point_0": {"hit": .8, "touch": .1, "none": .1},
              "point_1": {"hit": .8, "touch": .1, "none": .1}},
     "guess_correct", None, ["major", "qg", "point_0", "contradict"]),
    ("推理", {"qg": {"question": .01, "guess": .99},
              "point_0": {"hit": .8, "touch": .1, "none": .1},
              "point_1": {"hit": .8, "touch": .1, "none": .1}, "contradict": .5},
     "guess_close", None, ["major", "qg", "point_0", "contradict"]),
    ("推理", {"qg": {"question": .01, "guess": .99},
              "point_0": {"hit": .1, "touch": .3, "none": .6}},
     "guess_close", None, ["major", "qg", "point_0"]),
    ("推理", {"qg": {"question": .01, "guess": .99}, "kind": "q_open"},
     "guess_wrong", None, ["major", "qg", "point_0", "kind"]),
    ("推理", {"qg": {"question": .01, "guess": .99}}, "q_yesno", "no",
     ["major", "qg", "point_0", "kind", "quality", "answer"]),
    ("質問", {"point_0": {"hit": .8, "touch": .1, "none": .1},
              "point_1": {"hit": .8, "touch": .1, "none": .1}},
     "guess_correct", None, ["major", "qg", "kind", "point_0", "contradict"]),
])
def test_same_probabilities_preserve_every_stage_and_call_count(
    monkeypatch, problem, text, overrides, kind, answer, stages,
) -> None:
    payloads = _scripted_transport(monkeypatch, overrides)
    jev_result = jev.judge("c", text, problem, api_key="fake")
    dec_result = decisions.judge("c", text, problem, api_key="fake")
    assert (jev_result.kind, jev_result.answer) == (kind, answer)
    assert (dec_result.kind, dec_result.answer) == (kind, answer)
    assert (jev_result.reason, jev_result.bare_term) == (dec_result.reason, dec_result.bare_term)
    assert jev_result.debug["probabilities"] == dec_result.debug["probabilities"]
    assert jev_result.debug["calls"] == dec_result.debug["calls"] == len(stages)
    assert len(payloads["jev"]) == len(payloads["decisions"]) == len(stages)
    assert [next(iter(p["questions"])) for p in payloads["jev"]] == stages
    assert [p["questions"][0]["name"] for p in payloads["decisions"]] == stages
    for jev_payload, dec_payload in zip(payloads["jev"], payloads["decisions"]):
        assert dec_payload["input"] == json.dumps(jev_payload["state"], ensure_ascii=False)
        assert dec_payload["questions"] == decisions._questions(jev_payload["questions"])
    for key in ("input_tokens", "output_tokens", "latency_s"):
        assert jev_result.debug[key] == dec_result.debug[key]
    assert set(dec_result.debug) == set(jev_result.debug) | {"confidence", "refusals"}
    assert all(value == .01 for stage in dec_result.debug["confidence"].values()
               for value in stage.values())
    assert dec_result.method == "decisions"


def test_decisions_thresholds_can_be_tuned_without_changing_jev(monkeypatch, problem) -> None:
    _scripted_transport(monkeypatch, {
        "qg": {"question": .01, "guess": .99},
        "point_0": {"hit": .8, "touch": .1, "none": .1},
        "point_1": {"hit": .8, "touch": .1, "none": .1},
    })
    assert decisions.judge("c", "推理", problem, api_key="fake", t_point=.9).kind == "guess_close"
    assert jev.judge("c", "推理", problem, api_key="fake").kind == "guess_correct"
    assert decisions.judge("c", "推理", problem, api_key="fake").kind == "guess_correct"


def test_combiner_success_uses_openai_key_and_skips_other_judges(problem) -> None:
    outcome = Judgement("decisions", "q_yesno", "yes", bare_term=None)
    api = Mock(return_value=outcome)
    other = Mock(side_effect=AssertionError("other judge must not run"))
    result = combine("c", "same comment", problem, Config(judge_mode="decisions"),
                     {"openai_api_key": "fake-openai", "typesafe_api_key": "unused"},
                     decisions_call=api, luna_call=other, jev_call=other)
    api.assert_called_once_with(
        "c", "same comment", problem, api_key="fake-openai", model="gpt-6-luna",
    )
    other.assert_not_called()
    assert (result.kind, result.answer, result.decision) == ("q_yesno", "yes", "decisions")
    assert result.decisions == outcome and result.luna is None and result.jev is None
    assert result.mismatch is None and result.errors == []


@pytest.mark.parametrize("failure", [
    decisions.DecisionsError("refusal", debug={"refusals": {"count": 1, "names": ["quality"]}}),
    Judgement("decisions", None, error="bad response", debug={"input_tokens": 42}),
])
def test_combiner_failure_rejudges_same_comment_with_luna(problem, failure) -> None:
    dec = Mock(side_effect=failure) if isinstance(failure, Exception) else Mock(return_value=failure)
    luna = Mock(return_value=Judgement("luna", "q_yesno", "no"))
    result = combine("c", "same comment", problem, Config(judge_mode="decisions"),
                     {"openai_api_key": "fake"}, decisions_call=dec, luna_call=luna)
    luna.assert_called_once_with(
        "c", "same comment", problem, api_key="fake", model="gpt-6-luna",
    )
    assert result.decision == "decisions_fallback_luna" and result.answer == "no"
    assert result.decisions.error and result.decisions.debug == failure.debug
    assert result.errors == [f"decisions: {result.decisions.error}"]


def test_combiner_precomputed_and_luna_fallback_failure(problem) -> None:
    success = Judgement("decisions", "impression")
    result = combine("c", "text", problem, Config(judge_mode="decisions"), {},
                     precomputed={"decisions": success},
                     decisions_call=Mock(side_effect=AssertionError("precomputed only")))
    assert result.decisions == success
    with pytest.raises(RuntimeError, match="luna down"):
        combine("c", "text", problem, Config(judge_mode="decisions"), {},
                precomputed={"decisions": RuntimeError("decisions down"),
                             "luna": RuntimeError("luna down")})


def test_config_and_conditional_comment_log_preserve_legacy_shape(problem) -> None:
    assert Config.from_env({}).judge_mode == "hybrid"
    config = Config.from_env({"JUDGE_MODE": "decisions"})
    result = combine("c", "text", problem, config, {},
                     precomputed={"decisions": Judgement("decisions", "impression")})
    legacy = new_record({"id": "c", "text": "text"}, None, "now", Config(), problem)
    record = new_record({"id": "c", "text": "text"}, None, "now", config, problem)
    assert set(legacy["judgements"]) == {"luna", "jev"}
    apply_decision(record, result, Reply("ありがとう", "llm", False), judged_at="now")
    assert set(record["judgements"]) == {"luna", "jev", "decisions"}
    assert record["judgements"]["decisions"]["kind"] == "impression"


def test_local_trial_decisions_stub_mode_is_offline(tmp_path, monkeypatch) -> None:
    fixture = tmp_path / "stub.json"
    fixture.write_text(json.dumps([{
        "id": "dec-c", "comment": "感想", "luna": {"kind": "impression"},
        "jev": {"kind": "impression"}, "decisions": {"kind": "impression"},
    }], ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(http_util.request, "urlopen", Mock(side_effect=AssertionError("no HTTP")))
    monkeypatch.setattr(local_trial.Config, "from_env", lambda: Config())
    assert local_trial.main([
        "--problem", "U01", "--modes", "decisions", "--reply-variant", "2b",
        "--stub-judgements", str(fixture), "--out", str(tmp_path / "trial"),
    ]) == 0
    records = list((tmp_path / "trial" / "decisions").rglob("*.json"))
    assert len(records) == 1
    assert json.loads(records[0].read_text())["final"]["decision"] == "decisions"
