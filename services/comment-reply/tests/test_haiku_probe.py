"""Offline eight-pattern probe, frozen cache keys, usage and HTML reports."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from unittest.mock import Mock

import pytest

from app import anthropic_util, comment_log, http_util
from app.config import Config
from app.judge.combiner import Combined
from app.judge.contract import JudgeCriteria, Judgement, Problem
from app.reply.writer import Reply
from tools import build_probe_page, probe_metrics, probe_run


def _inputs(tmp_path: Path, problem: Problem) -> dict:
    files = [tmp_path / name for name in ("eval.json", "bare.json", "common.json")]
    for path, data in zip(files, ({"U01": [{"id": "U01-cached", "text": "病院に行った？",
                                           "kind": "q_yesno", "answer": "yes"}]}, {}, [])):
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return {"out": tmp_path / "work", "eval_path": files[0], "bare_term_path": files[1],
            "common_path": files[2], "problem_loader": lambda no: problem,
            "api_keys": {"anthropic_api_key": "fake-anthropic"},
            "run_at": "2026-10-08T00:00:00Z"}


def _debug(**changes) -> dict:
    return {"model": anthropic_util.MODEL, "input_tokens": 10, "output_tokens": 20,
            "cache_creation_input_tokens": 30, "cache_read_input_tokens": 40,
            "stop_reason": "end_turn", "latency_s": .2, **changes}


def _writer(combined, *args, **kwargs) -> Reply:
    debug = _debug() if kwargs["variant"] in {"1b-haiku", "1d-haiku"} else {}
    if debug:
        assert kwargs["anthropic_api_key"] == "fake-anthropic"
    return Reply("はい！" if combined.answer == "yes" else "いいえ。", "llm", False, debug=debug)


def test_eight_patterns_and_production_defaults(tmp_path, monkeypatch) -> None:
    assert probe_run.LEGACY_PATTERN_IDS == ("luna-1b", "luna-1d", "hybrid-1d", "jev-2b", "jev-2c")
    assert len(probe_run.PATTERNS) == 8
    assert probe_run.PATTERNS[6:] == (
        {"id": "haiku-1b", "label": "⑦ haiku + 1b-haiku", "judge_mode": "haiku",
         "reply_variant": "1b-haiku", "shadow": False, "consensus": False},
        {"id": "haiku-1d", "label": "⑧ haiku + 1d-haiku", "judge_mode": "haiku",
         "reply_variant": "1d-haiku", "shadow": False, "consensus": False},
    )
    config = Config.from_env({})
    assert (config.judge_mode, config.reply_variant) == ("hybrid", "1d-luna")
    for variant in ("1b-haiku", "1d-haiku"):
        config = Config.from_env({"JUDGE_MODE": "haiku", "REPLY_VARIANT": variant})
        assert (config.judge_mode, config.reply_variant) == ("haiku", variant)
    run = Mock()
    monkeypatch.setattr(probe_run, "run_probe", run)
    assert probe_run.main(["--out", str(tmp_path)]) == 0
    assert run.call_args.kwargs["patterns"] == list(probe_run.PATTERN_IDS)
    assert probe_run.main(["--patterns", "haiku-1d", "--problems", "U01", "U13"]) == 0
    assert run.call_args.kwargs["patterns"] == ["haiku-1d"]
    assert run.call_args.kwargs["problems"] == ["U01", "U13"]


def test_eight_pattern_probe_cache_and_page(tmp_path, monkeypatch, problem, capsys) -> None:
    args = _inputs(tmp_path, problem)
    luna = Mock(return_value=Judgement("luna", "q_yesno", "yes"))
    jev = Mock(return_value=Judgement("jev", "q_yesno", "no"))
    decisions = Mock(return_value=Judgement("decisions", "q_yesno", "yes"))
    haiku = Mock(return_value=Judgement("haiku", "q_yesno", "yes", debug=_debug()))
    writer = Mock(side_effect=_writer)
    results = probe_run.run_probe(
        **args, patterns=list(probe_run.PATTERN_IDS), luna_call=luna, jev_call=jev,
        decisions_call=decisions, haiku_call=haiku, writer_call=writer,
    )
    assert (luna.call_count, jev.call_count, decisions.call_count, haiku.call_count) == (1, 1, 1, 1)
    assert writer.call_count == 8
    haiku.assert_called_once_with("U01-cached", "病院に行った？", problem, api_key="fake-anthropic")
    assert set(results["rows"]) == set(probe_run.PATTERN_IDS)
    for pid in ("haiku-1b", "haiku-1d"):
        row = results["rows"][pid][0]
        assert row["record"]["final"]["decision"] == "haiku"
        assert row["record"]["reply"]["debug"]["output_tokens"] == 20
        assert row["cache"] == {"luna": "none", "jev": "none", "haiku": "miss", "writer": "miss"}
        assert row["timing"]["judge_s"] == row["timing"]["haiku_s"]
        assert row["timing"]["luna_s"] is None
    log = capsys.readouterr().out
    assert ("Anthropic: input_tokens=30, output_tokens=60, cache_creation_input_tokens=90, "
            "cache_read_input_tokens=120, refusals=0") in log
    before = {name: (args["out"] / name).read_bytes()
              for name in ("judge_cache.json", "writer_cache.json")}
    blocked = Mock(side_effect=AssertionError("cache must prevent every HTTP call"))
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    replay = probe_run.run_probe(
        **args, patterns=list(probe_run.PATTERN_IDS), luna_call=blocked, jev_call=blocked,
        decisions_call=blocked, haiku_call=blocked, writer_call=blocked,
    )
    blocked.assert_not_called()
    assert "new: input_tokens=0, output_tokens=0" in capsys.readouterr().out
    assert replay["rows"]["haiku-1b"][0]["cache"]["haiku"] == "hit"
    for name, content in before.items():
        assert (args["out"] / name).read_bytes() == content
    page = build_probe_page.build_page(replay, tmp_path / "probe.html")
    source = page.read_text(encoding="utf-8")
    body = (tmp_path / "probe" / "U01.html").read_text(encoding="utf-8")
    assert "8 パターン" in source and 'colspan="10"' in source
    for pattern in probe_run.PATTERNS:
        assert pattern["label"] in source and pattern["label"] in body
        assert f'id="pattern-{pattern["id"]}"' in body
        assert f"{pattern['label']}:" in source  # Each time-chart title includes this pattern.
    assert body.count('<h3>コメント</h3>') == 8
    assert len(list((tmp_path / "probe").glob("raw-*.js"))) == 8
    for text in ("拒否件数", "トークン（入力 / 出力 / キャッシュ）", "費用 USD", "応答時間",
                 "打ち切り max_tokens", "空応答", "Haiku から luna への再判定"):
        assert text in source


def test_haiku_is_not_called_for_existing_six_patterns(tmp_path, problem, capsys) -> None:
    args = _inputs(tmp_path, problem)
    args["api_keys"] = {}
    blocked = Mock(side_effect=AssertionError("Haiku not selected"))
    results = probe_run.run_probe(
        **args, patterns=list(probe_run.PATTERN_IDS[:6]),
        luna_call=lambda *a, **k: Judgement("luna", "q_yesno", "yes"),
        jev_call=lambda *a, **k: Judgement("jev", "q_yesno", "yes"),
        decisions_call=lambda *a, **k: Judgement("decisions", "q_yesno", "yes"),
        haiku_call=blocked, writer_call=_writer,
    )
    blocked.assert_not_called()
    assert "Anthropic:" not in capsys.readouterr().out
    assert all("haiku" not in row["record"]["judgements"]
               for rows in results["rows"].values() for row in rows)
    for count in (6, 5):
        legacy = deepcopy(results)
        legacy["meta"]["patterns"] = legacy["meta"]["patterns"][:count]
        legacy["rows"] = {p["id"]: legacy["rows"][p["id"]] for p in legacy["meta"]["patterns"]}
        page = build_probe_page.build_page(legacy, tmp_path / f"legacy-{count}.html")
        assert f"{count} パターン" in page.read_text(encoding="utf-8")
        assert "⑦ haiku + 1b-haiku" not in page.read_text(encoding="utf-8")
        body = (tmp_path / f"legacy-{count}" / "U01.html").read_text(encoding="utf-8")
        assert body.count('<h3>コメント</h3>') == count


def test_missing_anthropic_key_stops_before_any_judge(tmp_path, monkeypatch, problem) -> None:
    args = _inputs(tmp_path, problem)
    args["api_keys"] = {"openai_api_key": "fake-openai"}
    blocked = Mock(side_effect=AssertionError("missing-key validation must happen first"))
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        probe_run.run_probe(**args, patterns=["haiku-1d"])
    blocked.assert_not_called()


def test_refusal_cache_round_trip_preserves_category_and_luna_usage(tmp_path, monkeypatch, problem, capsys) -> None:
    args = _inputs(tmp_path, problem)
    debug = _debug(stop_reason="refusal", refusal_category="cyber", error_reason="refusal")
    haiku = Mock(side_effect=anthropic_util.AnthropicRefusalError("refused", debug=debug))
    luna = Mock(return_value=Judgement("luna", "q_yesno", "yes", debug={
        "prompt_tokens": 200, "completion_tokens": 30, "cached_tokens": 100,
    }))
    writer = Mock(return_value=Reply("はい！", "fallback_template", False, error="refused",
                                   debug=_debug(stop_reason="refusal", refusal_category="bio")))
    results = probe_run.run_probe(**args, patterns=["haiku-1b", "haiku-1d"],
                                 haiku_call=haiku, luna_call=luna, writer_call=writer)
    assert haiku.call_count == 1
    # The shared judge refusal is counted once in the run log and once in each pattern's metrics.
    assert "refusals=3" in capsys.readouterr().out
    row = results["rows"]["haiku-1d"][0]
    assert row["record"]["final"]["decision"] == "haiku_fallback_luna"
    assert row["timing"]["judge_s"] == pytest.approx(row["timing"]["haiku_s"] + row["timing"]["luna_s"])
    cached_haiku = next(entry for entry in json.loads((args["out"] / "judge_cache.json").read_text()).values()
                        if entry.get("exception", {}).get("type") == "AnthropicRefusalError")
    restored = probe_run._judge_outcome(cached_haiku)
    assert isinstance(restored, anthropic_util.AnthropicRefusalError) and restored.category == "cyber"
    assert restored.debug == debug
    blocked = Mock(side_effect=AssertionError("cached refusal must not retry HTTP"))
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    replay = probe_run.run_probe(**args, patterns=["haiku-1b", "haiku-1d"],
                                haiku_call=blocked, luna_call=blocked, writer_call=blocked)
    blocked.assert_not_called()
    assert "new: input_tokens=0, output_tokens=0" in capsys.readouterr().out
    assert replay["rows"]["haiku-1d"][0]["record"] == row["record"]
    api = probe_metrics.aggregate(replay)["patterns"]["haiku-1d"]["reference"]["api_usage"]
    assert api["haiku_fallback_luna"] == 1
    assert api["refusals"] == {"count": 2, "categories": {"bio": 1, "cyber": 1}}
    page = build_probe_page.build_page(replay, tmp_path / "refusal.html")
    assert "cyber: 1" in page.read_text(encoding="utf-8")
    assert "Haiku 失敗のため luna の判定" in (tmp_path / "refusal" / "U01.html").read_text(encoding="utf-8")


def test_frozen_six_pattern_cache_keys_replay_without_api(tmp_path, monkeypatch) -> None:
    """Seed literal pre-Haiku keys, including Decisions, rather than regenerating keys."""
    problem = Problem(
        3, "umigame-soup-1", "local-U01", "legacy-key", "男はなぜ泣いた？", "回復を知った",
        ("病院に行った",), ("回復",), JudgeCriteria((("回復を知った", "回復に触れた"),), ()),
        "回復したと知った。",
    )
    args = _inputs(tmp_path, problem)
    monkeypatch.setattr(probe_run, "PROMPT_VERSION", "cached-version")
    monkeypatch.setattr(comment_log, "PROMPT_VERSION", "cached-version")
    monkeypatch.setenv("LUNA_MODEL", "gpt-6-luna")
    judge_keys = {
        "luna": "f354800b3a205cb32b80a36ee8a74493b651f3a29a87d7840ac0f04ad9cb37a0",
        "jev": "a7be5ecc77fce29d4324fb196829074bec881fc7cf2051de902b1101234082ac",
        "decisions": "425ac4f1d60e9760bce5cba52206aa1c24db71f6a76504a134835da8e5802196",
    }
    writer_keys = (
        "dfae2f83f8151a54bcb4de81c83b09fe7ececc93edbc78d22f0cc53d6198dab6",
        "f322560970e59417064e57968160be54cdd1df103e6812e3e8448a1c3fd50e39",
        "2d5083b26929cafab35275c88dd716a8036c2cc99cdc2de51daff81cbcad2f2d",
        "4062b338f59e22efb972b8fa2d312dce685d16c77f52bc6f382e77d6e0eac27e",
        "f29d88eea7db5cf94f53e2b554bd749c7b2312617fea057fdbfad463adba713e",
        "a4a8afa08fe1c8a3bda641a579215e6fbcd1f4bcf1b6b6e86c978c39651670c2",
    )
    judge_cache = {key: {"judgement": asdict(Judgement(method, "q_yesno", "no" if method == "jev" else "yes")),
                         "elapsed_s": .4} for method, key in judge_keys.items()}
    writer_cache = {
        key: {"reply": asdict(Reply("いいえ。" if i in {3, 4} else "はい！", "llm", False)),
              "elapsed_s": .2} for i, key in enumerate(writer_keys)
    }
    case = {"id": "U01-cached", "text": "病院に行った？"}
    for method, key in judge_keys.items():
        assert probe_run._judge_cache_key(case, problem, method, "gpt-6-luna") == key
    for pattern, key in zip(probe_run.PATTERNS[:6], writer_keys):
        mode = pattern["judge_mode"]
        combined = Combined(None, None, "q_yesno", "no" if mode == "jev" else "yes",
                            None, "luna" if mode == "hybrid" else mode, None)
        assert probe_run._writer_cache_key(pattern, case, problem, combined, "gpt-6-luna") == key
    args["out"].mkdir()
    before = {}
    for name, value in (("judge_cache.json", judge_cache), ("writer_cache.json", writer_cache)):
        path = args["out"] / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        before[name] = path.read_bytes()
    blocked = Mock(side_effect=AssertionError("all six existing patterns must hit old caches"))
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    results = probe_run.run_probe(
        **args, patterns=list(probe_run.PATTERN_IDS[:6]), luna_call=blocked, jev_call=blocked,
        decisions_call=blocked, haiku_call=blocked, writer_call=blocked,
    )
    blocked.assert_not_called()
    for pid in probe_run.PATTERN_IDS[:6]:
        assert results["rows"][pid][0]["cache"]["writer"] == "hit"
    assert results["rows"]["dec-2c"][0]["cache"]["decisions"] == "hit"
    for name, content in before.items():
        assert (args["out"] / name).read_bytes() == content


def test_metrics_token_cost_refusal_failures_and_latency() -> None:
    """Use independent numeric costs and percentile expectations for both stages."""
    cases, rows = [], []
    for i in range(20):
        case = {"id": f"case-{i}", "no": "U01", "text": "質問", "expected_kind": "q_yesno",
                "expected_answer": "yes", "source": "eval", "accept_kinds": [], "accept_answers": []}
        cases.append(case)
        judgements = {}
        writer_debug = {}
        decision = "haiku"
        if i == 0:
            judgements = {
                "haiku": {"debug": {"usage": {
                    "input_tokens": 100, "output_tokens": 200,
                    "cache_creation_input_tokens": 40, "cache_read_input_tokens": 60,
                }, "stop_reason": "refusal", "refusal_category": "general_harms"}},
                "luna": {"debug": {"prompt_tokens": 2000, "completion_tokens": 100,
                                   "cached_tokens": 1000}},
            }
            writer_debug = {"usage": {"input_tokens": 50, "output_tokens": 80,
                                      "cache_creation_input_tokens": 10, "cache_read_input_tokens": 20}}
            decision = "haiku_fallback_luna"
        elif i == 1:
            judgements = {"haiku": {"debug": {"stop_reason": "max_tokens"}}}
            writer_debug = {"stop_reason": "refusal", "refusal_category": "cyber"}
        elif i in {2, 3}:
            reason = "missing_text" if i == 2 else "empty_text"
            judgements = {"haiku": {"debug": {"error_reason": reason}}}
            writer_debug = {"error_reason": reason}
        rows.append({"case_id": case["id"], "no": "U01", "record": {
            "final": {"kind": "q_yesno", "answer": "yes", "decision": decision},
            "judgements": judgements, "reply": {"text": "はい！", "source": "llm", "debug": writer_debug},
            "errors": [], "shadow_mismatch": None,
        }, "timing": {"judge_s": i + 1, "writer_s": 2 * (i + 1), "total_s": 3 * (i + 1)}})
    results = {"meta": {"patterns": [probe_run.PATTERNS[6]]}, "cases": cases, "rows": {"haiku-1b": rows}}
    original = deepcopy(results)
    report = probe_metrics.aggregate(results)["patterns"]["haiku-1b"]
    api = report["reference"]["api_usage"]
    judge, writer = api["judge"], api["writer"]
    assert {key: judge[key] for key in probe_metrics.TOKEN_FIELDS} == {
        "input_tokens": 2200, "output_tokens": 300,
        "cache_creation_input_tokens": 40, "cache_read_input_tokens": 1060,
    }
    assert {key: writer[key] for key in probe_metrics.TOKEN_FIELDS} == {
        "input_tokens": 80, "output_tokens": 80,
        "cache_creation_input_tokens": 10, "cache_read_input_tokens": 20,
    }
    assert judge["cost_usd"] == pytest.approx(.0002756)
    assert writer["cost_usd"] == pytest.approx(.00004645)
    assert api["cost_usd"] == pytest.approx(.00032205)
    assert judge["latency_s"] == {"median": 10.5, "p95": 19, "max": 20}
    assert writer["latency_s"] == {"median": 21, "p95": 38, "max": 40}
    assert api["refusals"] == {"count": 2, "categories": {"cyber": 1, "general_harms": 1}}
    assert api["max_tokens"] == 1 and api["empty_responses"] == 4
    assert judge["empty_response_reasons"] == {"empty_text": 1, "missing_text": 1}
    assert writer["empty_response_reasons"] == {"empty_text": 1, "missing_text": 1}
    assert api["haiku_fallback_luna"] == 1
    assert results == original
    # Telemetry adds reference values without changing any existing quality calculation.
    baseline = deepcopy(results)
    for row in baseline["rows"]["haiku-1b"]:
        row["record"].pop("judgements")
        row["record"]["reply"].pop("debug")
    assert probe_metrics.aggregate(baseline)["patterns"]["haiku-1b"]["metrics"] == report["metrics"]


def test_metrics_luna_native_cached_usage_and_decisions_input_only_cost() -> None:
    luna = probe_metrics._usage_summary([("luna", {"usage": {
        "prompt_tokens": 1_000_000, "completion_tokens": 1_000_000,
        "prompt_tokens_details": {"cached_tokens": 500_000},
    }})])
    assert luna["input_tokens"] == 1_000_000 and luna["cache_read_input_tokens"] == 500_000
    assert luna["cost_usd"] == pytest.approx(.555)
    decisions = probe_metrics._usage_summary([("decisions", {
        "input_tokens": 1_000_000, "output_tokens": 100, "refusals": {"count": 2, "names": ["a", "b"]},
    })])
    assert decisions["cost_usd"] == pytest.approx(.1)
    assert decisions["refusals"]["count"] == 2
    assert probe_metrics._usage_summary([("jev", {"input_tokens": 100})])["unpriced_methods"] == ["jev"]


def test_failed_judges_preserve_usage_in_records_and_cached_errors(tmp_path, monkeypatch, problem) -> None:
    args = _inputs(tmp_path, problem)
    haiku_debug = _debug(stop_reason="max_tokens", error_reason="max_tokens")
    luna_error = ValueError("Luna truncated")
    luna_error.debug = {"prompt_tokens": 20, "completion_tokens": 30, "finish_reason": "length"}
    luna = Mock(side_effect=luna_error)
    haiku = Mock(side_effect=anthropic_util.AnthropicError("Haiku truncated", debug=haiku_debug))
    blocked = Mock(side_effect=AssertionError("both judges failed; do not write"))
    results = probe_run.run_probe(**args, patterns=["haiku-1d"], luna_call=luna,
                                 haiku_call=haiku, writer_call=blocked)
    blocked.assert_not_called()
    row = results["rows"]["haiku-1d"][0]
    assert row["record"]["judgements"]["haiku"]["debug"] == haiku_debug
    assert row["record"]["judgements"]["luna"]["debug"] == luna_error.debug
    api = probe_metrics.aggregate(results)["patterns"]["haiku-1d"]["reference"]["api_usage"]
    assert api["max_tokens"] == 2 and api["judge"]["output_tokens"] == 50
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    replay = probe_run.run_probe(**args, patterns=["haiku-1d"], luna_call=blocked,
                                haiku_call=blocked, writer_call=blocked)
    blocked.assert_not_called()
    assert replay["rows"]["haiku-1d"][0]["record"] == row["record"]
