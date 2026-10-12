"""Offline checks for the local trial CLI (moved from comment-reply in 21-8c2)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from app import http_util
from app.config import Config
from app.judge.contract import Judgement
from app.reply import writer
from tools import local_trial


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
        assert saved["problem_schema_version"] == 4
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


def test_local_trial_haiku_mode_passes_effort(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(http_util.request, "urlopen", Mock(side_effect=AssertionError("no HTTP")))
    monkeypatch.setattr(local_trial.Config, "from_env", lambda: Config())
    monkeypatch.setenv("ANTHROPIC_API_KEY", "a")
    judge = Mock(return_value=Judgement("haiku", "impression", reason="感想"))
    monkeypatch.setattr(local_trial.haiku, "judge", judge)
    assert local_trial.main([
        "--problem", "U01", "--modes", "haiku", "--haiku-effort", "high",
        "--reply-variant", "2b", "--comment", "面白い", "--out", str(tmp_path / "trial"),
    ]) == 0
    assert judge.call_args.kwargs["effort"] == "high"
    records = list((tmp_path / "trial" / "haiku").rglob("*.json"))
    assert json.loads(records[0].read_text())["final"]["decision"] == "haiku"


def test_local_trial_patterns_reuse_each_judge_offline(tmp_path, monkeypatch) -> None:
    fixture = tmp_path / "stub.json"
    fixture.write_text(json.dumps([{
        "id": "p-c", "comment": "感想", "luna": {"kind": "impression"},
        "jev": {"kind": "impression"}, "haiku": {"kind": "impression"},
    }], ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(http_util.request, "urlopen", Mock(side_effect=AssertionError("no HTTP")))
    monkeypatch.setattr(local_trial.Config, "from_env", lambda: Config())
    assert local_trial.main([
        "--problem", "U01", "--patterns", "1", "2", "5", "7",
        "--stub-judgements", str(fixture), "--out", str(tmp_path / "trial"),
    ]) == 0
    dirs = sorted(path.name for path in (tmp_path / "trial").iterdir())
    assert dirs == ["p1-luna-1b", "p2-luna-1d-luna", "p5-jev-2c-luna", "p7-haiku-1b-haiku"]
    record = next((tmp_path / "trial" / "p7-haiku-1b-haiku").rglob("*.json"))
    assert json.loads(record.read_text())["final"]["decision"] == "haiku"


def test_local_trial_haiku_requires_anthropic_key(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(local_trial.Config, "from_env", lambda: Config())
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        local_trial.main(["--problem", "U01", "--patterns", "7", "--comment", "x",
                          "--out", str(tmp_path)])


def test_local_trial_runs_haiku_patterns_once_per_effort(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(http_util.request, "urlopen", Mock(side_effect=AssertionError("no HTTP")))
    monkeypatch.setattr(local_trial.Config, "from_env", lambda: Config())
    monkeypatch.setenv("ANTHROPIC_API_KEY", "a")
    judge = Mock(return_value=Judgement("haiku", "impression", reason="感想"))
    monkeypatch.setattr(local_trial.haiku, "judge", judge)
    assert local_trial.main([
        "--problem", "U01", "--modes", "haiku", "--haiku-effort", "max", "high",
        "--reply-variant", "2b", "--comment", "面白い", "--out", str(tmp_path / "trial"),
    ]) == 0
    assert [call.kwargs["effort"] for call in judge.call_args_list] == ["max", "high"]
    assert sorted(path.name for path in (tmp_path / "trial").iterdir()) == [
        "haiku-high", "haiku-max"]
