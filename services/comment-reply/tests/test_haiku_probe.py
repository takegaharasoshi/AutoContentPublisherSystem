"""Offline effort-specific Haiku probes, frozen legacy cache keys and reports."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from unittest.mock import Mock

import pytest

from app import anthropic_util, comment_log, http_util
from app.config import Config
from app.judge import haiku
from app.judge.combiner import Combined
from app.judge.contract import JudgeCriteria, Judgement, Problem
from app.reply import writer as reply_writer
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
        debug["effort"] = kwargs["haiku_effort"] if kwargs["variant"] == "1b-haiku" else "low"
    return Reply("はい！" if combined.answer == "yes" else "いいえ。", "llm", False, debug=debug)


def test_ten_patterns_cli_selection_and_production_defaults(tmp_path, monkeypatch) -> None:
    assert probe_run.LEGACY_PATTERN_IDS == ("luna-1b", "luna-1d", "hybrid-1d", "jev-2b", "jev-2c")
    assert len(probe_run.PATTERNS) == 10
    assert probe_run.PATTERNS[6:] == (
        *({"id": f"haiku-1b-{effort}", "label": f"⑦ haiku + 1b-haiku（{effort}）",
           "judge_mode": "haiku", "reply_variant": "1b-haiku", "shadow": False,
           "consensus": False, "haiku_effort": effort} for effort in ("max", "xhigh", "high")),
        {"id": "haiku-1d", "label": "⑧ haiku + 1d-haiku", "judge_mode": "haiku",
         "reply_variant": "1d-haiku", "shadow": False, "consensus": False, "haiku_effort": "max"},
    )
    config = Config.from_env({})
    assert (config.judge_mode, config.reply_variant) == ("hybrid", "1d-luna")
    for variant in ("1b-haiku", "1d-haiku"):
        config = Config.from_env({"JUDGE_MODE": "haiku", "REPLY_VARIANT": variant})
        assert (config.judge_mode, config.reply_variant) == ("haiku", variant)
    run = Mock()
    monkeypatch.setattr(probe_run, "run_probe", run)
    assert probe_run.main(["--out", str(tmp_path)]) == 0
    assert run.call_args.kwargs["patterns"] == [
        "luna-1b", "luna-1d", "jev-2c", "haiku-1b-max", "haiku-1b-xhigh", "haiku-1b-high",
    ]
    assert run.call_args.kwargs["workers"] == 4
    assert probe_run.main(["--patterns", "haiku-1d", "--problems", "U01", "U13"]) == 0
    assert run.call_args.kwargs["patterns"] == ["haiku-1d"]
    assert run.call_args.kwargs["problems"] == ["U01", "U13"]


def test_ten_pattern_probe_shares_judges_only_within_effort_and_builds_page(
    tmp_path, monkeypatch, problem, capsys,
) -> None:
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
    assert (luna.call_count, jev.call_count, decisions.call_count, haiku.call_count) == (1, 1, 1, 3)
    assert writer.call_count == 10
    assert {call.kwargs["effort"] for call in haiku.call_args_list} == {"max", "xhigh", "high"}
    for call in haiku.call_args_list:
        assert call.args == ("U01-cached", "病院に行った？", problem)
        assert call.kwargs["api_key"] == "fake-anthropic"
    assert set(results["rows"]) == set(probe_run.PATTERN_IDS)
    for pattern in probe_run.PATTERNS[6:]:
        row = results["rows"][pattern["id"]][0]
        assert row["record"]["final"]["decision"] == "haiku"
        assert row["record"]["reply"]["debug"]["output_tokens"] == 20
        assert row["cache"] == {"luna": "none", "jev": "none", "haiku": "miss", "writer": "miss"}
        assert row["timing"]["judge_s"] == row["timing"]["haiku_s"]
        assert row["timing"]["luna_s"] is None
        assert row["record"]["judgements"]["haiku"]["debug"]["effort"] == pattern["haiku_effort"]
        assert row["record"]["reply"]["debug"]["effort"] == (
            "low" if pattern["id"] == "haiku-1d" else pattern["haiku_effort"]
        )
    calls = [call for call in writer.call_args_list if call.kwargs["variant"] == "1b-haiku"]
    assert {call.kwargs["haiku_effort"] for call in calls} == {"max", "xhigh", "high"}
    log = capsys.readouterr().out
    for effort in ("max", "xhigh", "high"):
        assert (f"Anthropic ({effort}): input_tokens=20, output_tokens=40, "
                "cache_creation_input_tokens=60, cache_read_input_tokens=80, refusals=0") in log
    assert ("Anthropic (low): input_tokens=10, output_tokens=20, "
            "cache_creation_input_tokens=30, cache_read_input_tokens=40, refusals=0") in log
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
    for effort in ("max", "xhigh", "high"):
        assert replay["rows"][f"haiku-1b-{effort}"][0]["cache"]["haiku"] == "hit"
    for name, content in before.items():
        assert (args["out"] / name).read_bytes() == content
    page = build_probe_page.build_page(replay, tmp_path / "probe.html")
    source = page.read_text(encoding="utf-8")
    body = (tmp_path / "probe" / "U01.html").read_text(encoding="utf-8")
    assert "10 パターン" in source and 'colspan="12"' in source
    for pattern in probe_run.PATTERNS:
        assert pattern["label"] in source and pattern["label"] in body
        assert f'id="pattern-{pattern["id"]}"' in body
        assert f"{pattern['label']}:" in source  # Each time-chart title includes this pattern.
    assert body.count('<h3>コメント</h3>') == 10
    assert len(list((tmp_path / "probe").glob("raw-*.js"))) == 10
    for text in ("拒否件数", "トークン（入力 / 出力 / キャッシュ）", "費用 USD", "応答時間",
                 "打ち切り max_tokens", "空応答", "Haiku から luna への再判定"):
        assert text in source
    filtered = build_probe_page.exclude_patterns(replay, ["haiku-1b-xhigh", "haiku-1d"])
    assert filtered["meta"]["run_at"] == replay["meta"]["run_at"]
    kept_page = build_probe_page.build_page(filtered, tmp_path / "filtered.html")
    kept_source = kept_page.read_text(encoding="utf-8")
    assert "8 パターン" in kept_source
    assert "⑦ haiku + 1b-haiku（xhigh）" not in kept_source
    assert "⑦ haiku + 1b-haiku（max）" in kept_source
    assert "⑦ haiku + 1b-haiku（high）" in kept_source


def test_haiku_cache_keys_include_effort_and_only_their_own_template(
    tmp_path, monkeypatch, problem,
) -> None:
    case = {"id": "cache-test", "text": "病院に行った？"}
    combined = Combined(None, None, "q_yesno", "yes", None, "haiku", None)
    judge_path = tmp_path / "haiku_judge.txt"
    reply_path = tmp_path / "haiku_reply_1b.txt"
    for path in reply_writer.PROMPTS_DIR.glob("*.txt"):
        (tmp_path / path.name).write_bytes(path.read_bytes())
    monkeypatch.setattr(haiku, "RULES_PATH", judge_path)
    monkeypatch.setattr(probe_run, "PROMPTS_DIR", tmp_path)
    monkeypatch.setattr(comment_log, "PROMPTS_DIR", tmp_path)
    excluded = frozenset({"haiku_judge.txt", "haiku_reply_1b.txt"})
    legacy_version = comment_log.prompt_version(exclude_names=excluded)
    assert probe_run.PROMPT_VERSION == legacy_version
    keys = {effort: probe_run._judge_cache_key(case, problem, "haiku", "gpt-6-luna",
                                              haiku_effort=effort)
            for effort in ("max", "xhigh", "high")}
    assert len(set(keys.values())) == 3
    # Keep the pattern ID fixed so this checks the effort field itself.
    patterns = [{**probe_run.PATTERNS[6], "haiku_effort": effort}
                for effort in ("max", "xhigh", "high")]
    writer_keys = [probe_run._writer_cache_key(p, case, problem, combined, "gpt-6-luna")
                   for p in patterns]
    assert len(set(writer_keys)) == 3
    legacy_judges = {method: probe_run._judge_cache_key(case, problem, method, "gpt-6-luna")
                     for method in ("luna", "jev", "decisions")}
    legacy_writers = [probe_run._writer_cache_key(p, case, problem, combined, "gpt-6-luna")
                      for p in probe_run.PATTERNS[:6]]
    judge_path.write_text(judge_path.read_text(encoding="utf-8") + "\n判定の変更", encoding="utf-8")
    assert probe_run._judge_cache_key(case, problem, "haiku", "gpt-6-luna") != keys["max"]
    assert probe_run._writer_cache_key(patterns[0], case, problem, combined, "gpt-6-luna") == writer_keys[0]
    reply_path.write_text(reply_path.read_text(encoding="utf-8") + "\n返信の変更", encoding="utf-8")
    assert probe_run._writer_cache_key(patterns[0], case, problem, combined, "gpt-6-luna") != writer_keys[0]
    assert comment_log.prompt_version(exclude_names=excluded) == legacy_version
    for method, key in legacy_judges.items():
        assert probe_run._judge_cache_key(case, problem, method, "gpt-6-luna", haiku_effort="high") == key
    for pattern, key in zip(probe_run.PATTERNS[:6], legacy_writers):
        assert probe_run._writer_cache_key(pattern, case, problem, combined, "gpt-6-luna") == key
    one_d = probe_run.PATTERNS[-1]
    assert probe_run._writer_cache_key(one_d, case, problem, combined, "gpt-6-luna") == (
        probe_run._writer_cache_key({**one_d, "haiku_effort": "high"}, case, problem, combined, "gpt-6-luna")
    )


def test_incremental_same_out_keeps_caches_and_rebuilds_six_patterns_without_calls(
    tmp_path, problem,
) -> None:
    args = _inputs(tmp_path, problem)
    calls = {
        "luna_call": Mock(return_value=Judgement("luna", "q_yesno", "yes")),
        "jev_call": Mock(return_value=Judgement("jev", "q_yesno", "yes")),
        "haiku_call": Mock(return_value=Judgement("haiku", "q_yesno", "yes", debug=_debug())),
        "writer_call": Mock(side_effect=_writer),
    }
    # Include a Luna row with only high selected to catch accidental max-judge lookups.
    for pattern_ids in (["luna-1b", "haiku-1b-high"], ["haiku-1b-max"],
                        ["haiku-1b-xhigh"], ["luna-1d", "jev-2c"]):
        current = probe_run.run_probe(**args, patterns=pattern_ids, **calls)
        assert set(current["rows"]) == set(pattern_ids)
        saved = json.loads((args["out"] / "results.json").read_text(encoding="utf-8"))
        assert set(saved["rows"]) == set(pattern_ids)  # results are overwritten each time
    assert calls["haiku_call"].call_count == 3
    assert calls["luna_call"].call_count == calls["jev_call"].call_count == 1
    assert calls["writer_call"].call_count == 6
    blocked = Mock(side_effect=AssertionError("all patterns should be cached"))
    results = probe_run.run_probe(
        **args, patterns=list(probe_run.DEFAULT_PATTERN_IDS), luna_call=blocked, jev_call=blocked,
        haiku_call=blocked, writer_call=blocked,
    )
    blocked.assert_not_called()
    assert list(results["rows"]) == list(probe_run.DEFAULT_PATTERN_IDS)
    assert all(row["cache"]["writer"] == "hit" for rows in results["rows"].values() for row in rows)
    assert all(results["rows"][f"haiku-1b-{effort}"][0]["cache"]["haiku"] == "hit"
               for effort in ("max", "xhigh", "high"))
    page = build_probe_page.build_page(results, tmp_path / "six.html")
    assert "6 パターン" in page.read_text(encoding="utf-8")


def test_metrics_keep_three_efforts_cost_tokens_failures_and_latency_separate() -> None:
    cases = [{"id": f"case-{i}", "no": "U01", "text": "質問", "expected_kind": "q_yesno",
              "expected_answer": "yes", "source": "eval", "accept_kinds": [], "accept_answers": []}
             for i in range(20)]
    patterns = list(probe_run.PATTERNS[6:9])
    results = {"meta": {"patterns": patterns}, "cases": cases, "rows": {}}
    for scale, pattern in enumerate(patterns, 1):
        rows = []
        for i, case in enumerate(cases):
            judge = _debug(input_tokens=100 * scale, output_tokens=200 * scale,
                           cache_creation_input_tokens=40 * scale, cache_read_input_tokens=60 * scale,
                           effort=pattern["haiku_effort"])
            writer = _debug(input_tokens=50 * scale, output_tokens=80 * scale,
                            cache_creation_input_tokens=10 * scale, cache_read_input_tokens=20 * scale,
                            effort=pattern["haiku_effort"])
            if i < scale:
                judge.update(stop_reason="refusal", refusal_category="general_harms")
            elif 5 <= i < 5 + scale:
                judge["stop_reason"] = "max_tokens"
            if i < scale + 1:
                writer.update(stop_reason="refusal", refusal_category="cyber")
            elif 5 <= i < 9 - scale:
                writer["stop_reason"] = "max_tokens"
            rows.append({"case_id": case["id"], "no": "U01", "record": {
                "final": {"kind": "q_yesno", "answer": "yes", "decision": "haiku"},
                "judgements": {"haiku": {"debug": judge}},
                "reply": {"text": "はい！", "source": "llm", "debug": writer},
                "errors": [], "shadow_mismatch": None,
            }, "timing": {"judge_s": (i + 1) * scale, "writer_s": 2 * (i + 1) * scale,
                          "total_s": 3 * (i + 1) * scale}})
        results["rows"][pattern["id"]] = rows
    metrics = probe_metrics.aggregate(results)
    for scale, pattern in enumerate(patterns, 1):
        api = metrics["patterns"][pattern["id"]]["reference"]["api_usage"]
        judge, writer = api["judge"], api["writer"]
        assert judge["cost_usd"] == pytest.approx(.0001156 * 20 * scale)
        assert writer["cost_usd"] == pytest.approx(.00004645 * 20 * scale)
        assert judge["output_tokens"] == 4000 * scale
        assert writer["output_tokens"] == 1600 * scale
        assert judge["max_tokens"] == scale and writer["max_tokens"] == 4 - scale
        assert judge["refusals"]["count"] == scale
        assert writer["refusals"]["count"] == scale + 1
        assert judge["latency_s"] == {"median": 10.5 * scale, "p95": 19 * scale, "max": 20 * scale}
        assert writer["latency_s"] == {"median": 21 * scale, "p95": 38 * scale, "max": 40 * scale}


def test_effort_specific_failure_and_decisions_survive_cache_replay(tmp_path, problem) -> None:
    args = _inputs(tmp_path, problem)

    def judge(*args, effort, **kwargs):
        if effort == "high":
            raise anthropic_util.AnthropicError("truncated", debug=_debug(
                output_tokens=90, stop_reason="max_tokens", error_reason="max_tokens",
            ))
        return Judgement("haiku", "q_yesno", "yes" if effort == "max" else "no",
                         debug=_debug(output_tokens=10 if effort == "max" else 30))

    calls = {
        "haiku_call": Mock(side_effect=judge),
        "luna_call": Mock(return_value=Judgement("luna", "q_yesno", "no")),
        "writer_call": Mock(side_effect=_writer),
    }
    selected = [p["id"] for p in probe_run.PATTERNS[6:9]]
    results = probe_run.run_probe(**args, patterns=selected, **calls)
    assert calls["haiku_call"].call_count == 3
    for effort, decision, answer, output_tokens in (
        ("max", "haiku", "yes", 10), ("xhigh", "haiku", "no", 30),
        ("high", "haiku_fallback_luna", "no", 90),
    ):
        row = results["rows"][f"haiku-1b-{effort}"][0]
        assert row["record"]["final"] == {"kind": "q_yesno", "answer": answer, "decision": decision}
        api = probe_metrics.aggregate(results)["patterns"][f"haiku-1b-{effort}"]["reference"]["api_usage"]
        assert api["judge"]["output_tokens"] == output_tokens
        assert api["judge"]["max_tokens"] == int(effort == "high")
        assert row["record"]["judgements"]["haiku"]["debug"]["effort"] == effort
    blocked = Mock(side_effect=AssertionError("all efforts are cached"))
    replay = probe_run.run_probe(**args, patterns=selected, haiku_call=blocked,
                                luna_call=blocked, writer_call=blocked)
    blocked.assert_not_called()
    for pattern_id in selected:
        assert replay["rows"][pattern_id][0]["record"] == results["rows"][pattern_id][0]["record"]


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
    assert "Anthropic (" not in capsys.readouterr().out
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
    results = probe_run.run_probe(**args, patterns=["haiku-1b-max", "haiku-1d"],
                                 haiku_call=haiku, luna_call=luna, writer_call=writer)
    assert haiku.call_count == 1
    # The max judge is shared; the 1d writer's low usage is counted separately.
    log = capsys.readouterr().out
    assert "Anthropic (max):" in log and "refusals=2" in log
    assert "Anthropic (low):" in log and "refusals=1" in log
    row = results["rows"]["haiku-1d"][0]
    assert row["record"]["final"]["decision"] == "haiku_fallback_luna"
    assert row["timing"]["judge_s"] == pytest.approx(row["timing"]["haiku_s"] + row["timing"]["luna_s"])
    cached_haiku = next(entry for entry in json.loads((args["out"] / "judge_cache.json").read_text()).values()
                        if entry.get("exception", {}).get("type") == "AnthropicRefusalError")
    restored = probe_run._judge_outcome(cached_haiku)
    assert isinstance(restored, anthropic_util.AnthropicRefusalError) and restored.category == "cyber"
    assert restored.debug == {**debug, "effort": "max"}
    blocked = Mock(side_effect=AssertionError("cached refusal must not retry HTTP"))
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    replay = probe_run.run_probe(**args, patterns=["haiku-1b-max", "haiku-1d"],
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
    legacy_pattern = {**probe_run.PATTERNS[6], "id": "haiku-1b", "label": "⑦ haiku + 1b-haiku"}
    legacy_pattern.pop("haiku_effort")
    results = {"meta": {"patterns": [legacy_pattern]}, "cases": cases, "rows": {"haiku-1b": rows}}
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
    assert row["record"]["judgements"]["haiku"]["debug"] == {**haiku_debug, "effort": "max"}
    assert row["record"]["judgements"]["luna"]["debug"] == luna_error.debug
    api = probe_metrics.aggregate(results)["patterns"]["haiku-1d"]["reference"]["api_usage"]
    assert api["max_tokens"] == 2 and api["judge"]["output_tokens"] == 50
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    replay = probe_run.run_probe(**args, patterns=["haiku-1d"], luna_call=blocked,
                                haiku_call=blocked, writer_call=blocked)
    blocked.assert_not_called()
    assert replay["rows"]["haiku-1d"][0]["record"] == row["record"]


LEGACY_HAIKU_RESULTS = probe_run.SERVICE_DIR / "work/probe/full-20261008-8p-merged/results.json"


@pytest.mark.skipif(not LEGACY_HAIKU_RESULTS.is_file(), reason="local legacy Haiku results not present")
def test_saved_legacy_haiku_results_build_page_and_cli_exclusions(tmp_path) -> None:
    before = LEGACY_HAIKU_RESULTS.read_bytes()
    results = json.loads(before)
    assert "haiku-1b" in results["rows"]
    page = build_probe_page.build_page(results, tmp_path / "legacy-haiku.html")
    source = page.read_text(encoding="utf-8")
    assert "8 パターン" in source and "⑦ haiku + 1b-haiku" in source
    assert "⑦ haiku + 1b-haiku（high）" not in source
    assert build_probe_page.main([
        "--results", str(LEGACY_HAIKU_RESULTS), "--out", str(tmp_path / "legacy-filtered.html"),
        "--exclude-patterns", "dec-2c", "haiku-1d",
    ]) == 0
    source = (tmp_path / "legacy-filtered.html").read_text(encoding="utf-8")
    assert "6 パターン" in source and "⑦ haiku + 1b-haiku" in source
    assert "⑥ decisions + 2c-luna" not in source and "⑧ haiku + 1d-haiku" not in source
    assert LEGACY_HAIKU_RESULTS.read_bytes() == before
