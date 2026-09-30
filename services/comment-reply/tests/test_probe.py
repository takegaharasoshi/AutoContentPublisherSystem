"""Offline checks for the production-path comment reply probe."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from app.comment_log import new_record
from app.config import Config
from app.judge.contract import Judgement, Problem
from app.reply import templates
from app.reply.writer import Reply
from tools import build_probe_page, probe_metrics, probe_run


def _write_data(path: Path, eval_data: dict, bare: dict | None = None,
                common: list | None = None) -> tuple[Path, Path, Path]:
    path.mkdir(parents=True, exist_ok=True)
    files = (path / "eval_problems.json", path / "bare_term_cases.json",
             path / "common_cases.json")
    for target, data in zip(files, (eval_data, bare or {}, common or [])):
        target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return files


def _offline_problem(no: str) -> Problem:
    return Problem.from_snapshot({
        "schema_version": 2, "set_code": "umigame-soup-1", "media_id": "media-" + no,
        "content_key": "key-" + no, "problem_text": f"{no} の問題文",
        "truth": "真相", "fact_sheet": ["確定事実"], "core_points": ["核心"],
        "reveal_text": "開示文",
    })


def _offline_run(tmp_path: Path) -> tuple[dict, dict[str, int], Path, dict]:
    paths = _write_data(tmp_path / "data", {
        "U01": [{"id": "U01-e01", "text": "<b>関係ある？</b>",
                 "kind": "q_yesno", "answer": "yes"}],
        "U13": [{"id": "U13-e01", "text": "正解を当てた", "kind": "guess_correct"}],
    })
    counts = {"luna": 0, "jev": 0, "writer": 0}

    def luna_call(comment_id, text, problem, *, api_key, model):
        counts["luna"] += 1
        return Judgement("luna", "q_yesno", "yes") if comment_id.startswith("U01") else Judgement(
            "luna", "guess_correct")

    def jev_call(comment_id, text, problem, *, api_key):
        counts["jev"] += 1
        if comment_id.startswith("U13"):
            raise RuntimeError("offline Jev failure")
        return Judgement("jev", "q_yesno", "no")

    def writer_call(combined, comment_id, text, problem, *, variant, openai_api_key, model):
        counts["writer"] += 1
        if combined.kind == "q_yesno":
            return Reply("はい！</script><b>返信</b>", "llm", False)
        return Reply("正解です！", "llm", False)

    out = tmp_path / "work"
    args = {"out": out, "eval_path": paths[0], "bare_term_path": paths[1],
            "common_path": paths[2], "problem_loader": _offline_problem,
            "luna_call": luna_call, "jev_call": jev_call, "writer_call": writer_call,
            "api_keys": {}, "run_at": "2026-10-01T00:00:00Z"}
    results = probe_run.run_probe(**args)
    return results, counts, out, args


def _case(case_id: str, kind: str, answer: str | None = None,
          no: str = "U01", text: str = "質問") -> dict:
    return {"id": case_id, "no": no, "text": text, "expected_kind": kind,
            "expected_answer": answer, "accept_kinds": [], "accept_answers": [],
            "source": "eval"}


def _row(case: dict, kind: str | None, answer: str | None = None,
         reply: str | None = None, decision: str | None = "luna") -> dict:
    return {"case_id": case["id"], "no": case["no"],
            "record": {"final": {"kind": kind, "answer": answer, "decision": decision},
                       "reply": {"text": reply, "source": "template"},
                       "errors": [], "shadow_mismatch": None},
            "timing": {"total_s": 1.0, "judge_s": .4, "writer_s": .6}}


def _aggregate(cases: list[dict], rows: list[dict]) -> dict:
    data = {"meta": {"patterns": [{"id": "test"}]}, "cases": cases,
            "rows": {"test": rows}}
    return probe_metrics.aggregate(data)["patterns"]["test"]


def test_load_cases_round_robin_bare_and_duplicate(tmp_path):
    paths = _write_data(tmp_path, {
        "U01": [{"id": "a", "text": "A", "kind": "q_yesno", "answer": "yes"}],
        "U13": [{"id": "b", "text": "B", "kind": "impression"}],
    }, {"_note": "ignored", "U01": [{"id": "bare", "text": "語", "kind": "q_open"}]},
        [{"id": "c1", "text": "共通1", "kind": "greeting"},
         {"id": "c2", "text": "共通2", "kind": "greeting"},
         {"id": "c3", "text": "共通3", "kind": "greeting"}])
    cases = probe_run.load_cases(eval_path=paths[0], bare_term_path=paths[1],
                                 common_path=paths[2])
    assert [(x["id"], x["no"], x["source"]) for x in cases] == [
        ("a", "U01", "eval"), ("bare", "U01", "bare_term"),
        ("b", "U13", "eval"), ("c1", "U01", "common"),
        ("c2", "U13", "common"), ("c3", "U01", "common")]
    duplicate = [{"id": "a", "text": "duplicate", "kind": "greeting"}]
    paths[2].write_text(json.dumps(duplicate), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate case id"):
        probe_run.load_cases(eval_path=paths[0], bare_term_path=paths[1],
                             common_path=paths[2])


def test_run_cache_timing_record_and_offline_page(tmp_path):
    results, counts, out, args = _offline_run(tmp_path)
    assert counts == {"luna": 2, "jev": 2, "writer": 10}
    assert all(len(rows) == 2 for rows in results["rows"].values())
    hybrid = results["rows"]["hybrid-1d"][0]
    assert hybrid["timing"]["judge_s"] == max(hybrid["timing"]["luna_s"],
                                                 hybrid["timing"]["jev_s"])
    fallback = results["rows"]["jev-2c"][1]
    assert fallback["record"]["final"]["decision"] == "jev_fallback_luna"
    assert fallback["timing"]["judge_s"] == pytest.approx(
        fallback["timing"]["jev_s"] + fallback["timing"]["luna_s"])
    config = Config(judge_mode="luna", shadow=False, consensus=False,
                    reply_variant="1b", set_code="umigame-soup-1")
    baseline = new_record({"id": "U01-e01", "text": "<b>関係ある？</b>",
                           "from": {"id": "probe"}, "media": {"id": "media-U01"}},
                          None, "2026-10-01T00:00:00Z", config, _offline_problem("U01"))
    assert set(results["rows"]["luna-1b"][0]["record"]) == set(baseline)
    assert (out / "results.json").is_file() and (out / "metrics.json").is_file()

    second = probe_run.run_probe(**args)
    assert counts == {"luna": 2, "jev": 2, "writer": 10}
    assert second["rows"]["hybrid-1d"][0]["cache"] == {
        "luna": "hit", "jev": "hit", "writer": "hit"}
    page = tmp_path / "page" / "probe.html"
    assert build_probe_page.main(["--results", str(out / "results.json"),
                                  "--out", str(page)]) == 0
    source = page.read_text(encoding="utf-8")
    assert '<h2 id="summary">1. サマリー</h2>' in source
    assert '<h2 id="patterns">2. パターン別の結果</h2>' in source
    assert len(re.findall(r'<h3 id="pattern-', source)) == 5
    assert len(re.findall(r'<h4 id="problem-', source)) == 10
    assert source.count('<h5>コメント</h5>') == 10
    assert source.count('<h5>テスト結果生データ</h5>') == 10
    assert len(list((page.parent / page.stem).glob("raw-*.js"))) == 10
    assert not re.search(r'(?:src|href)="https?://', source)
    assert "&lt;b&gt;関係ある？&lt;/b&gt;" in source
    assert "<b>関係ある？</b>" not in source
    raw = (page.parent / page.stem / "raw-luna-1b-U01.js").read_text(encoding="utf-8")
    assert 'window.PROBE_RAW["luna-1b/U01"] = ' in raw
    assert "<\\/script>" in raw
    previous = source
    stale = page.parent / page.stem / "raw-stale.js"
    stale.write_text("old", encoding="utf-8")
    build_probe_page.build_page(second, page)
    assert page.read_text(encoding="utf-8") == previous
    assert not stale.exists()


def test_combine_error_keeps_row(tmp_path, monkeypatch):
    results, _, _, args = _offline_run(tmp_path)
    original = probe_run.combine

    def failing_combine(comment_id, *rest, **kwargs):
        if comment_id == "U01-e01":
            raise RuntimeError("synthetic combine failure")
        return original(comment_id, *rest, **kwargs)

    monkeypatch.setattr(probe_run, "combine", failing_combine)
    args["out"] = tmp_path / "failed"
    failure = probe_run.run_probe(**args)
    assert len(failure["rows"]["luna-1b"]) == 2
    row = failure["rows"]["luna-1b"][0]
    assert row["record"]["final"]["kind"] is None
    assert row["record"]["errors"] == ["processing: RuntimeError: synthetic combine failure"]
    assert results["rows"]["luna-1b"][0]["record"]["final"]["kind"] == "q_yesno"


def test_luna_only_skips_jev_and_missing_key_stops_before_calls(tmp_path):
    paths = _write_data(tmp_path / "data", {
        "U01": [{"id": "only", "text": "質問", "kind": "q_yesno", "answer": "yes"}]})
    calls = {"luna": 0, "writer": 0}

    def luna_call(comment_id, text, problem, *, api_key, model):
        calls["luna"] += 1
        return Judgement("luna", "q_yesno", "yes")

    def jev_call(*args, **kwargs):
        raise AssertionError("Jev must not run")

    def writer_call(combined, comment_id, text, problem, *, variant, openai_api_key, model):
        calls["writer"] += 1
        return Reply("はい！", "template", False)

    args = {"out": tmp_path / "work", "patterns": ["luna-1b"],
            "eval_path": paths[0], "bare_term_path": paths[1], "common_path": paths[2],
            "problem_loader": _offline_problem, "luna_call": luna_call,
            "jev_call": jev_call, "api_keys": {}}
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        probe_run.run_probe(**args)
    assert calls == {"luna": 0, "writer": 0}
    result = probe_run.run_probe(**args, writer_call=writer_call)
    assert calls == {"luna": 1, "writer": 1}
    assert result["rows"]["luna-1b"][0]["cache"]["jev"] == "none"


def test_metrics_p3_per_problem_limit():
    cases = [_case(f"q-{i:03}", "q_yesno", "yes") for i in range(100)]
    rows = [_row(case, "q_yesno", "no" if i < 3 else "yes", "はい！")
            for i, case in enumerate(cases)]
    metric = _aggregate(cases, rows)["metrics"]["P3"]
    assert metric["count"] == 3 and metric["rate"] == pytest.approx(.03)
    assert metric["by_problem"] == {"U01": 3}
    assert metric["pass"] is False


def test_metrics_p6_all_four_conditions():
    cases = [_case("t", "troll"), _case("a", "abuse"), _case("s", "spam"),
             _case("p", "personal_info"), _case("o", "impression")]
    clean = [_row(cases[0], "troll", reply=templates.pick("troll", "t")),
             _row(cases[1], "abuse", reply=templates.pick("abuse", "a")),
             _row(cases[2], "spam"), _row(cases[3], "personal_info"),
             _row(cases[4], "impression", reply="ありがとう")]
    assert _aggregate(cases, clean)["metrics"]["P6"]["pass"] is True
    bad = [_row(cases[0], "troll", reply="はい。"), _row(cases[1], "abuse", reply="違う"),
           _row(cases[2], "spam", reply="返信した"), _row(cases[3], "personal_info"),
           _row(cases[4], "spam")]
    metric = _aggregate(cases, bad)["metrics"]["P6"]
    assert metric["pass"] is False
    assert metric["details"] == {
        "restricted_openers": 1, "template": 0, "no_reply_violation": 1,
        "ordinary_restricted": 1, "template_total": 2, "template_rate": 0.0,
        "ordinary_total": 1, "ordinary_rate": 1.0}


def test_metrics_l1_kind_opener_and_answer_synonym():
    cases = [_case(f"q{i}", "q_yesno", "yes") for i in range(95)]
    cases.extend(_case(f"i{i}", "impression") for i in range(5))
    rows = [_row(case, "q_yesno", "yes", "はい！") for case in cases[:95]]
    rows.extend(_row(case, "impression" if i < 4 else "chat", reply="ありがとう")
                for i, case in enumerate(cases[95:]))
    report = _aggregate(cases, rows)
    assert report["metrics"]["L1_kind"]["pass"] is True
    assert report["metrics"]["L1_kind"]["by_kind"]["impression"]["rate"] == .8
    rows[-2] = _row(cases[-2], "chat", reply="ありがとう")
    report = _aggregate(cases, rows)
    assert report["metrics"]["L1_kind"]["rate"] > .9
    assert report["metrics"]["L1_kind"]["pass"] is False

    q_cases = [_case("yes", "q_yesno", "yes"), _case("bad", "q_yesno", "yes")]
    q_rows = [_row(q_cases[0], "q_yesno", "yes", "はい！"),
              _row(q_cases[1], "q_yesno", "yes", "たぶんそう")]
    assert _aggregate(q_cases, q_rows)["metrics"]["L2_opener"]["pass"] is False
    assert probe_metrics.answer_matches({"expected_answer": "irrelevant", "answer": "no",
                                         "comment_text": "関係ある？"}) is True
    assert probe_metrics.answer_matches({"expected_answer": "irrelevant", "answer": "no",
                                         "comment_text": "誰なの？"}) is False
    alternative = _case("alt", "q_yesno", "yes")
    alternative["accept_answers"] = ["no"]
    assert probe_metrics.row_flags(_row(alternative, "q_yesno", "no", "いいえ。"),
                                   alternative)["label_mismatch"] is False


def test_metrics_recognize_production_correct_and_unknown_openers():
    cases = [_case("right", "guess_correct"), _case("wrong", "guess_wrong"),
             _case("unknown", "q_yesno", "irrelevant", text="これは重要？")]
    rows = [_row(cases[0], "guess_correct", reply="正解！開示文"),
            _row(cases[1], "guess_correct", reply="正解！開示文"),
            _row(cases[2], "q_yesno", "unknown",
                 templates.YESNO_OPENERS["unknown"] + "また聞いてね")]
    report = _aggregate(cases, rows)
    assert report["metrics"]["P5"]["count"] == 1
    assert report["metrics"]["P2"]["count"] == 1
    assert report["metrics"]["L2_opener"]["pass"] is True
