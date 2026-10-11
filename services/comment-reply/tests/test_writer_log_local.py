"""Offline writer, record, and local CLI integration checks."""

from __future__ import annotations

import json
import logging
from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock

import pytest

from app import comment_log
from app.config import Config
from app.judge.combiner import Combined
from app.judge.contract import JudgeCriteria, Judgement
from app.reply import templates, writer
from tools import local_trial


def _combined(kind: str, answer: str | None = None,
              term: str | None = None, decision: str = "luna") -> Combined:
    result = Judgement("luna", kind, answer=answer, bare_term=term)
    return Combined(result, None, kind, answer, term, decision)


@pytest.mark.parametrize("variant", ["1b", "1d-luna", "2b", "2c-luna"])
def test_writer_forced_replies_and_correct_disclosure(monkeypatch, variant, problem) -> None:
    calls = []

    def llm(*args, **kwargs):
        calls.append(kwargs)
        return "正解！LLM が真相を説明", {"model": "fake"}

    monkeypatch.setattr(writer, "_llm_reply", llm)
    assert writer.write_reply(_combined("spam"), "1", "宣伝", problem, variant=variant).source == "no_reply"
    troll = writer.write_reply(_combined("troll"), "1", "!?", problem, variant=variant)
    assert troll.text in templates.TEMPLATES["troll"] and troll.source == "template"
    correct = writer.write_reply(_combined("guess_correct"), "1", "推理", problem, variant=variant,
                                 openai_api_key="fake")
    if variant == "1b":
        assert correct.text == "正解！LLM が真相を説明" and correct.source == "llm"
        assert calls[0]["variant"] == "1b"
    else:
        assert correct.text == templates.CORRECT_PREFIX + problem.reveal_text
        assert correct.source == "template"


def test_writer_yesno_guard_bare_term_and_over_80(monkeypatch, caplog, problem) -> None:
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs: ("そうかも", {}))
    with caplog.at_level(logging.WARNING):
        guarded = writer.write_reply(_combined("q_yesno", "yes"), "1", "質問", problem,
                                     variant="1d-luna", openai_api_key="fake")
    assert guarded.source == "fallback_template" and guarded.text.startswith("はい！")
    assert "REPLY_WRITER_FALLBACK" in caplog.text

    bare = writer.write_reply(_combined("q_open", term="レントゲン"), "1", "レントゲン？", problem,
                              variant="2b")
    assert "レントゲン" in bare.text and ("何" in bare.text or "どう" in bare.text)
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs: ("はい！" + "長" * 90, {}))
    with caplog.at_level(logging.WARNING):
        long = writer.write_reply(_combined("q_yesno", "yes"), "1", "質問", problem,
                                  variant="1d-luna", openai_api_key="fake")
    assert long.over_80 and len(long.text) > 80
    assert "REPLY_OVER_80" in caplog.text


@pytest.mark.parametrize("variant", ["1b", "1d-luna", "2b", "2c-luna"])
def test_bare_term_question_in_every_variant(monkeypatch, variant, problem) -> None:
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs: ("レントゲン、なるほどね。", {}))
    result = writer.write_reply(
        _combined("q_open", term="レントゲン"), "1", "レントゲン？", problem,
        variant=variant, openai_api_key="fake",
    )
    assert result.text is not None and "レントゲン" in result.text
    assert "何" in result.text or "どう" in result.text
    assert result.source == ("template" if variant == "2b" else "fallback_template")


def test_template_variety_and_bare_prompt(problem) -> None:
    for kind, options in templates.TEMPLATES.items():
        if kind in {"guess_correct", "spam", "personal_info"}:
            continue
        assert len(set(options)) >= 3, kind
    assert len(set(templates.BARE_TERM_QUESTIONS)) >= 3
    result = _combined("q_open", term="レントゲン")
    prompt = writer._render_prompt(
        "{kind} / {bare_term} / {style}", result, problem, False,
        style="style", slot="slot",
    )
    assert prompt == "q_open / レントゲン / style"


@pytest.mark.parametrize("variant", ["1b", "1d-luna", "2b", "2c-luna"])
def test_writer_prompt_excludes_judge_criteria(variant, problem) -> None:
    hidden = ("HIT_PRIVATE_1", "TOUCH_PRIVATE_1", "ERROR_PRIVATE_1")
    private_problem = replace(problem, judge_criteria=JudgeCriteria(
        ((hidden[0], hidden[1]),) + problem.judge_criteria.points[1:], (hidden[2],)
    ))
    with_truth = variant == "1b"
    prompt_name = "reply_1b_with_truth.txt" if with_truth else "reply_writer.txt"
    template = (writer.PROMPTS_DIR / prompt_name).read_text(encoding="utf-8")
    prompt = writer._render_prompt(
        template, _combined("guess_close"), private_problem, with_truth,
        style="style", slot="slot",
    )
    assert all(secret not in prompt for secret in hidden)


@pytest.mark.parametrize("variant,effort,max_tokens,with_truth", [
    ("1b", "xhigh", 2400, True),
    ("1b", "medium", 2400, True),
    ("1d-luna", "low", 800, False),
    ("2c-luna", "low", 800, False),
])
def test_writer_request_variant_contract(monkeypatch, variant, effort, max_tokens, with_truth, problem) -> None:
    requests = []

    def post(req, **kwargs):
        requests.append(json.loads(req.data))
        return {"choices": [{"finish_reason": "stop", "message": {"content": '{"reply":"はい！"}'}}]}

    monkeypatch.setattr(writer, "post_json_with_retry", post)
    result = writer.write_reply(
        _combined("q_yesno", "yes"), "1", "質問", problem,
        variant=variant, openai_api_key="fake", model="dated-model",
        haiku_effort="high", luna_effort=effort if variant == "1b" else "max",
    )
    assert result.source == "llm"
    payload = requests[0]
    assert payload["model"] == "dated-model"
    assert payload["reasoning_effort"] == effort
    assert payload["max_completion_tokens"] == max_tokens
    assert payload["messages"][1]["content"] == "質問"
    template_name = "reply_1b_with_truth.txt" if with_truth else "reply_writer.txt"
    expected = writer._render_prompt(
        (writer.PROMPTS_DIR / template_name).read_text(encoding="utf-8"),
        _combined("q_yesno", "yes"), problem, with_truth,
        style=(writer.PROMPTS_DIR / "reply_style.txt").read_text(encoding="utf-8"),
        slot=writer.pick_slot("1"),
    )
    assert payload["messages"][0]["content"] == expected
    assert (problem.truth in payload["messages"][0]["content"]) is with_truth
    assert "temperature" not in payload


def test_record_schema_and_local_sink_exclude_username(tmp_path, problem) -> None:
    comment = {"id": "comment-1", "text": "レントゲン？",
               "from": {"id": "user-id", "username": "do-not-store"},
               "media": {"id": "media-1"}}
    record = comment_log.new_record(
        comment, 1700000000, "2026-09-30T10:00:00Z", Config(), problem,
    )
    combined = _combined("q_open", term="レントゲン")
    reply = writer.write_reply(combined, "comment-1", comment["text"], problem, variant="2b")
    comment_log.apply_decision(record, combined, reply)
    required = {"schema_version", "comment_id", "parent_id", "media_id", "set_code",
                "content_key", "problem_schema_version", "commenter_id", "text", "times",
                "config", "judgements", "final", "reply", "errors",
                "fact_sheet_hash"}
    assert required <= record.keys()
    assert record["schema_version"] == 1
    assert "shadow_mismatch" not in record
    assert "shadow" not in record["config"] and "consensus" not in record["config"]
    assert record["config"]["haiku_effort"] == "high"
    assert record["config"]["luna_effort"] == "xhigh"
    assert record["times"]["comment_created_at"].endswith("Z")
    assert len(record["config"]["prompt_version"]) == 12
    assert len(record["fact_sheet_hash"]) == 12
    path = Path(comment_log.write_record(record, directory=tmp_path))
    assert path.is_file()
    saved = path.read_text(encoding="utf-8")
    assert "username" not in saved and "do-not-store" not in saved
    assert "comment-log/umigame-soup-1/dt=2026-09-30/comment-1.json" in str(path)


def test_local_trial_stub_writes_three_mode_records_without_keys(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    sample = Path(local_trial.__file__).parent / "sample_stub_U01.json"
    assert local_trial.main([
        "--problem", "U01", "--stub-judgements", str(sample),
        "--reply-variant", "2b", "--out", str(tmp_path),
    ]) == 0
    files = list(tmp_path.rglob("*.json"))
    assert len(files) == 18
    assert {path.relative_to(tmp_path).parts[0] for path in files} == {"luna", "jev", "haiku"}
    for mode in ("luna", "jev", "haiku"):
        saved = json.loads(next((tmp_path / mode).rglob("local-u01-split.json")).read_text())
        assert saved["final"]["decision"] == mode
        assert "shadow_mismatch" not in saved
        assert saved["reply"]["source"] == "template"


def test_local_trial_passes_configured_haiku_effort_to_writer(tmp_path, monkeypatch, problem) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "fake-openai")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-anthropic")
    monkeypatch.setenv("HAIKU_EFFORT", "high")
    monkeypatch.setattr(local_trial, "_load_stock_problem", lambda no: problem)
    monkeypatch.setattr(local_trial.luna, "judge", Mock(return_value=Judgement("luna", "q_yesno", "yes")))
    call = Mock(return_value=writer.Reply("はい！", "llm", False))
    monkeypatch.setattr(local_trial, "write_reply", call)
    assert local_trial.main([
        "--problem", "U01", "--comment", "質問", "--modes", "luna",
        "--reply-variant", "1b-haiku", "--out", str(tmp_path),
    ]) == 0
    assert call.call_args.kwargs["haiku_effort"] == "high"
    assert call.call_args.kwargs["anthropic_api_key"] == "fake-anthropic"
    assert call.call_args.kwargs["variant"] == "1b-haiku"


@pytest.mark.parametrize("mode,pattern", [("luna", "9"), ("jev", "10")])
def test_local_new_patterns_use_independent_haiku_writer(tmp_path, monkeypatch, mode, pattern) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "openai")
    monkeypatch.setenv("TYPESAFE_API_KEY", "jev")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic")
    judge = Mock(return_value=Judgement(mode, "q_yesno", "yes"))
    monkeypatch.setattr(getattr(local_trial, mode), "judge", judge)
    blocked = Mock(side_effect=AssertionError("main succeeded"))
    monkeypatch.setattr(local_trial.haiku, "judge", blocked)
    call = Mock(return_value=writer.Reply("はい！", "llm", False))
    monkeypatch.setattr(local_trial, "write_reply", call)
    assert local_trial.main(["--problem", "U01", "--patterns", pattern, "--comment", "質問",
                             "--out", str(tmp_path)]) == 0
    judge.assert_called_once()
    blocked.assert_not_called()
    assert call.call_args.kwargs["variant"] == "1b-haiku"
    assert call.call_args.kwargs["haiku_effort"] == "high"
    record = json.loads(next(tmp_path.rglob("*.json")).read_text())
    assert record["final"]["decision"] == mode


def test_local_luna_efforts_are_forwarded_and_cached(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "openai")
    judge = Mock(return_value=Judgement("luna", "q_yesno", "yes"))
    monkeypatch.setattr(local_trial.luna, "judge", judge)
    call = Mock(return_value=writer.Reply("はい！", "llm", False))
    monkeypatch.setattr(local_trial, "write_reply", call)
    assert local_trial.main(["--problem", "U01", "--patterns", "1", "2", "--comment", "質問",
                             "--luna-effort", "max", "high", "--out", str(tmp_path)]) == 0
    assert [c.kwargs["effort"] for c in judge.call_args_list] == ["max", "high"]
    assert [c.kwargs["luna_effort"] for c in call.call_args_list] == ["max", "high", "max", "high"]
    assert len(list(tmp_path.rglob("*.json"))) == 4


@pytest.mark.parametrize("mode,fallback", [("luna", "haiku"), ("jev", "haiku"), ("haiku", "luna")])
def test_local_calls_fallback_only_after_main_failure(tmp_path, monkeypatch, mode, fallback) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "openai")
    monkeypatch.setenv("TYPESAFE_API_KEY", "jev")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic")
    order = []

    def main(*a, **k):
        order.append(mode)
        raise ValueError("main failed")

    def sub(*a, **k):
        assert order == [mode]
        order.append(fallback)
        assert k["effort"] == ("high" if fallback == "haiku" else "xhigh")
        return Judgement(fallback, "impression")

    monkeypatch.setattr(getattr(local_trial, mode), "judge", main)
    monkeypatch.setattr(getattr(local_trial, fallback), "judge", sub)
    assert local_trial.main(["--problem", "U01", "--modes", mode, "--reply-variant", "2b",
                             "--comment", "感想", "--out", str(tmp_path)]) == 0
    record = json.loads(next(tmp_path.rglob("*.json")).read_text())
    assert order == [mode, fallback]
    assert record["final"]["decision"] == f"{mode}_fallback_{fallback}"
    assert record["judgements"][mode]["error"] == "main failed"
