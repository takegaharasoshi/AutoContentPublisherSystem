"""Offline sixth-pattern, frozen cache and legacy report compatibility checks."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from unittest.mock import Mock

import pytest

from app import comment_log, http_util
from app.judge import decisions
from app.judge.contract import JudgeCriteria, Judgement, Problem
from app.reply.writer import Reply
from tools import build_probe_page, probe_metrics, probe_run


def _inputs(tmp_path: Path, problem: Problem) -> dict:
    paths = [tmp_path / name for name in ("eval.json", "bare.json", "common.json")]
    data = [{"U01": [{"id": "U01-cached", "text": "病院に行った？",
                      "kind": "q_yesno", "answer": "yes"}]}, {}, []]
    for path, value in zip(paths, data):
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    return {"out": tmp_path / "work", "eval_path": paths[0], "bare_term_path": paths[1],
            "common_path": paths[2], "problem_loader": lambda no: problem,
            "api_keys": {}, "run_at": "2026-10-08T00:00:00Z"}


def _writer(combined, *args, **kwargs) -> Reply:
    return Reply("はい！" if combined.answer == "yes" else "いいえ。", "llm", False)


def test_six_patterns_cli_defaults_and_explicit_selection(tmp_path, monkeypatch) -> None:
    assert len(probe_run.PATTERNS) == 6
    assert probe_run.PATTERNS[-1] == {
        "id": "dec-2c", "label": "⑥ decisions + 2c-luna", "judge_mode": "decisions",
        "shadow": False, "consensus": False, "reply_variant": "2c-luna",
    }
    run = Mock(return_value={})
    monkeypatch.setattr(probe_run, "run_probe", run)
    assert probe_run.main(["--out", str(tmp_path)]) == 0
    assert run.call_args.kwargs["patterns"] == list(probe_run.PATTERN_IDS)
    assert probe_run.main(["--patterns", "dec-2c", "--out", str(tmp_path)]) == 0
    assert run.call_args.kwargs["patterns"] == ["dec-2c"]


def test_six_patterns_usage_cache_replay_and_page(tmp_path, monkeypatch, problem, capsys) -> None:
    args = _inputs(tmp_path, problem)
    luna = Mock(return_value=Judgement("luna", "q_yesno", "yes"))
    jev = Mock(return_value=Judgement("jev", "q_yesno", "no"))
    dec = Mock(return_value=Judgement("decisions", "q_yesno", "yes", debug={
        "model": "gpt-6-luna", "calls": 4, "input_tokens": 80, "output_tokens": 0,
        "latency_s": .3, "probabilities": {}, "confidence": {"A1": {"major": .01}},
        "refusals": {"count": 0, "names": []},
    }))
    writer = Mock(side_effect=_writer)
    results = probe_run.run_probe(
        **args, patterns=list(probe_run.PATTERN_IDS), luna_call=luna, jev_call=jev,
        decisions_call=dec, writer_call=writer,
    )
    assert (luna.call_count, jev.call_count, dec.call_count, writer.call_count) == (1, 1, 1, 6)
    log = capsys.readouterr().out
    assert "Decisions: input_tokens=80, calls=4 (new: input_tokens=80, calls=4)" in log
    row = results["rows"]["dec-2c"][0]
    assert row["record"]["final"]["decision"] == "decisions"
    assert row["cache"] == {"luna": "none", "jev": "none", "decisions": "miss", "writer": "miss"}
    assert row["timing"]["judge_s"] == row["timing"]["decisions_s"]
    assert row["timing"]["luna_s"] is None
    metrics = probe_metrics.aggregate(results)
    assert metrics["patterns"]["dec-2c"]["reference"]["decisions_usage"] == {
        "input_tokens": 80, "output_tokens": 0, "calls": 4,
        "refusals": {"count": 0, "names": []},
    }
    assert set(results["rows"]) == set(probe_run.PATTERN_IDS)
    before = {name: (args["out"] / name).read_bytes()
              for name in ("judge_cache.json", "writer_cache.json")}
    blocked = Mock(side_effect=AssertionError("cache replay must not call an API"))
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    replay = probe_run.run_probe(
        **args, patterns=list(probe_run.PATTERN_IDS), luna_call=blocked, jev_call=blocked,
        decisions_call=blocked, writer_call=blocked,
    )
    assert "new: input_tokens=0, calls=0" in capsys.readouterr().out
    blocked.assert_not_called()
    assert replay["rows"]["dec-2c"][0]["cache"]["decisions"] == "hit"
    page = tmp_path / "probe.html"
    build_probe_page.build_page(replay, page)
    source = page.read_text(encoding="utf-8")
    body = (tmp_path / "probe" / "U01.html").read_text(encoding="utf-8")
    assert "6 パターン" in source and "⑥ decisions + 2c-luna" in source
    assert "Decisions 入力トークン" in source
    assert 'id="pattern-dec-2c"' in body and "Decisions の判定" in body
    assert body.count('<h3>コメント</h3>') == 6
    assert len(list((tmp_path / "probe").glob("raw-*.js"))) == 6

    legacy = probe_run.run_probe(
        **args, patterns=list(probe_run.LEGACY_PATTERN_IDS), luna_call=blocked,
        jev_call=blocked, decisions_call=blocked, writer_call=blocked,
    )
    blocked.assert_not_called()
    assert "Decisions:" not in capsys.readouterr().out
    for pid in probe_run.LEGACY_PATTERN_IDS:
        assert legacy["rows"][pid] == replay["rows"][pid]
        assert set(legacy["rows"][pid][0]["record"]["judgements"]) == {"luna", "jev"}
        assert set(legacy["rows"][pid][0]["cache"]) == {"luna", "jev", "writer"}
        assert "decisions_s" not in legacy["rows"][pid][0]["timing"]
    for name, content in before.items():
        assert (args["out"] / name).read_bytes() == content


def test_refusal_fallback_usage_survives_cached_exception(tmp_path, problem) -> None:
    args = _inputs(tmp_path, problem)
    debug = {"calls": 1, "input_tokens": 42, "output_tokens": 0, "latency_s": .2,
             "confidence": {"A1": {}}, "refusals": {"count": 1, "names": ["major"]}}
    dec = Mock(side_effect=decisions.DecisionsError("refusal", debug=debug))
    luna = Mock(return_value=Judgement("luna", "q_yesno", "yes"))
    results = probe_run.run_probe(
        **args, patterns=["dec-2c"], decisions_call=dec, luna_call=luna,
        writer_call=_writer,
    )
    row = results["rows"]["dec-2c"][0]
    assert row["record"]["final"]["decision"] == "decisions_fallback_luna"
    assert row["record"]["judgements"]["decisions"]["debug"] == debug
    assert row["timing"]["judge_s"] == pytest.approx(
        row["timing"]["decisions_s"] + row["timing"]["luna_s"]
    )
    blocked = Mock(side_effect=AssertionError("cached fallback only"))
    cached = probe_run.run_probe(
        **args, patterns=["dec-2c"], decisions_call=blocked, luna_call=blocked,
        writer_call=blocked,
    )
    blocked.assert_not_called()
    assert cached["rows"]["dec-2c"][0]["record"] == row["record"]
    usage = probe_metrics.aggregate(cached)["patterns"]["dec-2c"]["reference"]["decisions_usage"]
    assert usage["input_tokens"] == 42 and usage["calls"] == 1
    assert usage["refusals"] == {"count": 1, "names": ["major"]}
    assert build_probe_page._decision("decisions_fallback_luna") == "Decisions 失敗のため luna の判定"


def test_frozen_legacy_cache_keys_and_five_pattern_results(tmp_path, monkeypatch) -> None:
    """Use fixed hashes and the pre-Decisions JSON shapes, with every API blocked."""
    problem = Problem(
        3, "umigame-soup-1", "local-U01", "legacy-key", "男はなぜ泣いた？", "回復を知った",
        ("病院に行った",), ("回復",), JudgeCriteria((("回復を知った", "回復に触れた"),), ()),
        "回復したと知った。",
    )
    args = _inputs(tmp_path, problem)
    monkeypatch.setattr(probe_run, "PROMPT_VERSION", "cached-version")
    monkeypatch.setattr(comment_log, "PROMPT_VERSION", "cached-version")
    monkeypatch.setenv("LUNA_MODEL", "gpt-6-luna")
    judge_cache = {
        "f354800b3a205cb32b80a36ee8a74493b651f3a29a87d7840ac0f04ad9cb37a0": {
            "judgement": asdict(Judgement("luna", "q_yesno", "yes")), "elapsed_s": .4},
        "a7be5ecc77fce29d4324fb196829074bec881fc7cf2051de902b1101234082ac": {
            "judgement": asdict(Judgement("jev", "q_yesno", "no")), "elapsed_s": .3},
    }
    writer_keys = (
        "dfae2f83f8151a54bcb4de81c83b09fe7ececc93edbc78d22f0cc53d6198dab6",
        "f322560970e59417064e57968160be54cdd1df103e6812e3e8448a1c3fd50e39",
        "2d5083b26929cafab35275c88dd716a8036c2cc99cdc2de51daff81cbcad2f2d",
        "4062b338f59e22efb972b8fa2d312dce685d16c77f52bc6f382e77d6e0eac27e",
        "f29d88eea7db5cf94f53e2b554bd749c7b2312617fea057fdbfad463adba713e",
    )
    writer_cache = {
        key: {"reply": asdict(Reply("はい！" if i < 3 else "いいえ。", "llm", False)),
              "elapsed_s": .2} for i, key in enumerate(writer_keys)
    }
    args["out"].mkdir()
    before = {}
    for name, cache in (("judge_cache.json", judge_cache), ("writer_cache.json", writer_cache)):
        target = args["out"] / name
        target.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        before[name] = target.read_bytes()
    blocked = Mock(side_effect=AssertionError("legacy cache must be reused"))
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    results = probe_run.run_probe(
        **args, patterns=list(probe_run.LEGACY_PATTERN_IDS), luna_call=blocked,
        jev_call=blocked, decisions_call=blocked, writer_call=blocked,
    )
    blocked.assert_not_called()
    assert [p["id"] for p in results["meta"]["patterns"]] == list(probe_run.LEGACY_PATTERN_IDS)
    for i, pid in enumerate(probe_run.LEGACY_PATTERN_IDS):
        row = results["rows"][pid][0]
        assert row["record"]["final"] == {
            "kind": "q_yesno", "answer": "yes" if i < 3 else "no",
            "decision": "luna" if i < 3 else "jev",
        }
        assert row["cache"]["writer"] == "hit"
    for name, content in before.items():
        assert (args["out"] / name).read_bytes() == content
    # A metadata-only sixth entry must not create an empty phantom pattern.
    results["meta"]["patterns"].append(probe_run.PATTERNS[-1])
    page = build_probe_page.build_page(results, tmp_path / "legacy.html")
    assert "5 パターン" in page.read_text(encoding="utf-8")
    assert "⑥ decisions + 2c-luna" not in page.read_text(encoding="utf-8")
    body = (tmp_path / "legacy" / "U01.html").read_text(encoding="utf-8")
    assert body.count('<h3>コメント</h3>') == 5


LEGACY_WORK = probe_run.SERVICE_DIR / "work/probe/full-20261004"


@pytest.mark.skipif(
    not (LEGACY_WORK / "results.json").is_file(), reason="local saved probe not present",
)
def test_saved_work_caches_decode_and_old_results_generate_page(tmp_path, monkeypatch) -> None:
    before = {name: (LEGACY_WORK / name).read_bytes()
              for name in ("judge_cache.json", "writer_cache.json", "results.json")}
    cache = json.loads(before["judge_cache.json"])
    for entry in cache.values():
        outcome = probe_run._judge_outcome(entry)
        if "judgement" in entry:
            assert asdict(outcome) == entry["judgement"]
    results = json.loads(before["results.json"])
    blocked = Mock(side_effect=AssertionError("legacy page must not call HTTP"))
    monkeypatch.setattr(http_util.request, "urlopen", blocked)
    page = build_probe_page.build_page(results, tmp_path / "saved.html")
    assert "5 パターン" in page.read_text(encoding="utf-8")
    for no in results["meta"]["problems"]:
        body = (tmp_path / "saved" / f"{no}.html").read_text(encoding="utf-8")
        assert body.count('<h3>コメント</h3>') == 5
        assert 'id="pattern-dec-2c"' not in body
    blocked.assert_not_called()
    for name, content in before.items():
        assert (LEGACY_WORK / name).read_bytes() == content
