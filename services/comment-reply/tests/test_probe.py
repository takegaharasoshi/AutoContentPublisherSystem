"""Offline checks for the production-path comment reply probe."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
import random
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from app.comment_log import new_record
from app.config import Config
from app.judge.contract import JudgeCriteria, KINDS, Judgement, Problem
from app.reply import templates
from app.reply.writer import Reply
from tools import build_probe_page, contradiction_sweep, probe_metrics, probe_run
from tools.local_trial import _load_stock_problem


def _write_data(path: Path, eval_data: dict, bare: dict | None = None,
                common: list | None = None) -> tuple[Path, Path, Path]:
    path.mkdir(parents=True, exist_ok=True)
    files = (path / "eval_problems.json", path / "bare_term_cases.json",
             path / "common_cases.json")
    for target, data in zip(files, (eval_data, bare or {}, common or [])):
        target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return files


def _offline_problem(no: str) -> Problem:
    return replace(
        _load_stock_problem(no), media_id="media-" + no,
        content_key="key-" + no, problem_text=f"{no} の問題文",
        truth="真相", fact_sheet=("確定事実",), reveal_text="開示文",
    )


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


def _review_results() -> dict:
    cases = []
    for index in range(24):
        cases.append(_case(f"imp-{index:02}", "impression", no="U01" if index % 2 else "U13"))
    cases.extend([
        _case("q-yes", "q_yesno", "yes", no="U01", text="関係ある？"),
        _case("q-yes-b", "q_yesno", "yes", no="U13", text="そうなの？"),
        _case("q-irrelevant", "q_yesno", "irrelevant", no="U01", text="重要ですか？"),
        _case("q-no", "q_yesno", "no", no="U13", text="誰ですか？"),
        _case("multi", "q_multi", no="U01"),
        _case("open", "q_open", no="U13"),
        _case("correct", "guess_correct", no="U01"),
        _case("wrong", "guess_wrong", no="U13"),
    ])
    cases.extend(_case(f"kind-{kind}", kind, no="U01" if i % 2 else "U13")
                 for i, kind in enumerate(KINDS)
                 if kind not in {"q_yesno", "q_multi", "q_open", "guess_correct",
                                 "impression", "guess_wrong"})
    patterns = [{"id": f"pattern-{i}", "label": f"パターン {i}",
                 "judge_mode": "hybrid" if i == 1 else "luna"} for i in range(1, 4)]
    rows: dict[str, list[dict]] = {}
    for pattern_index, pattern in enumerate(patterns):
        pattern_rows = []
        for case in cases:
            kind, answer, reply = case["expected_kind"], case["expected_answer"], "ありがとう"
            if case["id"].startswith("imp-") and int(case["id"].split("-")[1]) % 4 == 0:
                kind, reply = "chat", "同じ返事"
            elif case["id"] in {"q-yes", "q-yes-b"}:
                kind, answer = "q_yesno", ("no" if pattern_index != 2 else "yes")
                reply = "はい。"
            elif case["id"] == "q-irrelevant":
                kind, answer, reply = "q_yesno", "no", "関係ありません。"
            elif case["id"] == "q-no":
                kind, answer, reply = "q_yesno", "irrelevant", "関係ない。"
            elif case["id"] == "multi":
                kind, answer, reply = ("q_open", None, "答えです") if pattern_index == 1 else (
                    "q_multi", None, "一つ目はこうです")
            elif case["id"] == "open":
                kind, answer, reply = "q_open", None, "答えです"
            elif case["id"] == "correct":
                kind, answer, reply = "guess_correct", None, "正解です！"
            elif case["id"] == "wrong":
                kind, answer, reply = "guess_correct", None, "正解！"
            elif case["expected_kind"] in templates.NO_REPLY_KINDS:
                kind, answer, reply = case["expected_kind"], None, None
            else:
                answer = None
            item = _row(case, kind, answer, reply)
            item["timing"] = {"total_s": 1.0, "judge_s": .4, "writer_s": .6}
            pattern_rows.append(item)
        rows[pattern["id"]] = pattern_rows
    per_problem = {no: sum(case["no"] == no for case in cases) for no in ("U01", "U13")}
    return {
        "meta": {"run_at": "2026-10-04T00:00:00Z", "patterns": patterns,
                 "problems": ["U01", "U13"],
                 "case_counts": {no: {"eval": count, "bare_term": 0, "common": 0}
                                 for no, count in per_problem.items()},
                 "prompt_version": "test", "luna_model": "test"},
        "cases": cases, "rows": rows,
        "problems": {no: {"problem_text": f"{no} test"} for no in per_problem},
    }


def _review_scenarios(results: dict) -> list[set[str]]:
    data = build_probe_page._review_data(results, probe_metrics.aggregate(results))
    keys = [pair["key"] for pair in data["pairs"]]
    rng = random.Random(2106)
    scenarios = [set(), set(keys)]
    for fraction in (.2, .5, .8):
        count = round(len(keys) * fraction)
        scenarios.append(set(rng.sample(keys, count)))
    return scenarios


def _assert_review_js_matches_python(results: dict,
                                     leak_decisions: dict[str, str] | None = None) -> None:
    if not shutil.which("node"):
        pytest.skip("node is not installed")
    baseline = probe_metrics.aggregate(results)
    data = build_probe_page._review_data(results, baseline)
    scenarios = _review_scenarios(results)
    source = (build_probe_page.REVIEW_CORE + "\nvar payload = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
              + "\nconsole.log(JSON.stringify(payload.sets.map(function (keys) {"
              + " return reviewMetrics(payload.data, keys, payload.leak_decisions); })));\n")
    payload = json.dumps({"data": data, "sets": [sorted(keys) for keys in scenarios],
                          "leak_decisions": leak_decisions or {}},
                         ensure_ascii=False, separators=(",", ":"))
    completed = subprocess.run(["node", "-e", source], input=payload, check=True,
                               capture_output=True, text=True)
    actual = json.loads(completed.stdout)
    for accepted, browser_result in zip(scenarios, actual):
        report = probe_metrics.aggregate(results, accepted, leak_decisions)
        for pattern in results["meta"]["patterns"]:
            pattern_id = pattern["id"]
            python_report = report["patterns"][pattern_id]
            browser_pattern = browser_result[pattern_id]
            for key in build_probe_page.REVIEW_RECALCULATED:
                item = python_report["metrics"][key]
                value = build_probe_page._ja_note(item["value"]) if key == "L1_kind_each" else item["value"]
                assert {name: browser_pattern[key][name] for name in ("value", "pass")} == {
                    "value": value, "pass": item["pass"]}
            python_kinds = {}
            kind_items = python_report["metrics"]["L1_kind_each"]["kinds"]
            for kind in KINDS:
                if kind in probe_metrics.QUESTION_KINDS:
                    continue
                item = kind_items[kind]
                value = (f"{item['rate']:.1%}（{item['count']}/{item['total']}）"
                         if item["rate"] is not None else "対象なし")
                python_kinds[kind] = {"value": value, "pass": item["pass"]}
            assert browser_pattern["L1_kind_each"]["kinds"] == python_kinds
            assert browser_pattern["yesno"] == {
                name: {"value": python_report["reference"]["yesno_accuracy"][name]["value"]}
                for name in ("existing", "new")
            }
            assert browser_pattern["passCount"] == sum(
                item["pass"] is True for item in python_report["metrics"].values())


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
    assert '<h2 id="problems">2. 問題ごとのページ</h2>' in source
    assert '<table class="case-table">' not in source
    page_dir = page.parent / page.stem
    problem_pages = sorted(page_dir.glob("*.html"))
    assert [p.name for p in problem_pages] == ["U01.html", "U13.html"]
    for problem_page in problem_pages:
        assert f'href="{page.stem}/{problem_page.name}"' in source
        body = problem_page.read_text(encoding="utf-8")
        assert len(re.findall(r'<h2 id="pattern-', body)) == 5
        assert body.count('<h3>コメント</h3>') == 5
        assert body.count('<h3>テスト結果生データ</h3>') == 5
        assert 'href="../../../assets/style.css"' in body
        assert not re.search(r'(?:src|href)="https?://', body)
    assert len(list(page_dir.glob("raw-*.js"))) == 10
    assert not re.search(r'(?:src|href)="https?://', source)
    u01 = (page_dir / "U01.html").read_text(encoding="utf-8")
    assert "&lt;b&gt;関係ある？&lt;/b&gt;" in u01
    assert "<b>関係ある？</b>" not in u01
    # 合否表の NG の ID は、問題ごとのページに実在する行へのリンクになっている
    row_ids = {(p.name, rid) for p in problem_pages
               for rid in re.findall(r'<tr id="([^"]+)"', p.read_text(encoding="utf-8"))}
    ng_links = re.findall(r'class="ng-link" href="[^"/]+/([^"#]+)#([^"]+)"', source)
    assert ng_links and set(ng_links) <= row_ids
    assert '<table class="eval-table">' in source
    raw = (page.parent / page.stem / "raw-luna-1b-U01.js").read_text(encoding="utf-8")
    assert 'window.PROBE_RAW["luna-1b/U01"] = ' in raw
    assert "<\\/script>" in raw
    previous = source
    stale = page.parent / page.stem / "raw-stale.js"
    stale.write_text("old", encoding="utf-8")
    stale_page = page.parent / page.stem / "U99.html"
    stale_page.write_text("old", encoding="utf-8")
    build_probe_page.build_page(second, page)
    assert page.read_text(encoding="utf-8") == previous
    assert not stale.exists() and not stale_page.exists()


def test_probe_cache_key_changes_with_judge_criteria() -> None:
    problem = _offline_problem("U01")
    changed = replace(problem, judge_criteria=JudgeCriteria(
        (("新しい当てた基準", "新しい触れた基準"),)
        + problem.judge_criteria.points[1:], problem.judge_criteria.errors
    ))
    case = {"text": "コメント"}
    assert probe_run._content_hash(case, problem) != probe_run._content_hash(case, changed)


def test_contradiction_sweep_displays_old_and_new_point_probabilities() -> None:
    assert contradiction_sweep._point_display(0.5) == "0.50"
    assert contradiction_sweep._point_display({"hit": 0.5, "close": 0.8}) == (
        "hit=0.50/close=0.80"
    )


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
    assert report["metrics"]["L1_kind_each"]["pass"] is True
    assert report["metrics"]["L1_kind"]["by_kind"]["impression"]["rate"] == .8
    rows[-2] = _row(cases[-2], "chat", reply="ありがとう")
    report = _aggregate(cases, rows)
    assert report["metrics"]["L1_kind"]["rate"] > .9
    assert report["metrics"]["L1_kind"]["pass"] is True
    assert report["metrics"]["L1_kind_each"]["pass"] is False
    assert set(report["metrics"]["L1_kind_each"]["by_kind"]) == {"impression"}
    assert [x["id"] for x in report["metrics"]["L1_kind_each"]["ng"]] == ["i3", "i4"]
    kinds = report["metrics"]["L1_kind_each"]["kinds"]
    assert "q_yesno" not in kinds and kinds["impression"]["pass"] is False
    assert [x["id"] for x in kinds["impression"]["ng"]] == ["i3", "i4"]

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


def test_metrics_recognize_production_correct_and_irrelevant_openers():
    cases = [_case("right", "guess_correct"), _case("wrong", "guess_wrong"),
             _case("irrelevant", "q_yesno", "irrelevant", text="これは重要？")]
    rows = [_row(cases[0], "guess_correct", reply="正解！開示文"),
            _row(cases[1], "guess_correct", reply="正解！開示文"),
            _row(cases[2], "q_yesno", "irrelevant",
                 templates.YESNO_OPENERS["irrelevant"] + "また聞いてね")]
    report = _aggregate(cases, rows)
    assert report["metrics"]["P5"]["count"] == 1
    assert report["metrics"]["P2"]["count"] == 1
    assert report["metrics"]["L2_opener"]["pass"] is True


def test_aggregate_acceptance_matches_adding_alternate_labels():
    results = _review_results()
    assert probe_metrics.aggregate(results) == probe_metrics.aggregate(results, frozenset())
    for case_id in ("q-yes", "multi"):
        target_row = next(row for row in results["rows"]["pattern-1"]
                          if row["case_id"] == case_id)
        final = target_row["record"]["final"]
        accepted_key = probe_metrics.pair_key(target_row["case_id"], final["kind"], final["answer"])
        actual = probe_metrics.aggregate(results, {accepted_key})
        expanded = deepcopy(results)
        case = next(case for case in expanded["cases"] if case["id"] == target_row["case_id"])
        case["accept_kinds"].append(final["kind"])
        if final["kind"] == "q_yesno" and final["answer"]:
            case["accept_answers"].append(final["answer"])
        assert actual == probe_metrics.aggregate(expanded)


def test_apply_labels_yesno_alternate_kind_limited_to_accepted_answers():
    case = {"expected_kind": "guess_wrong", "expected_answer": None,
            "accept_kinds": ["q_yesno"], "accept_answers": ["no"]}
    accepted = probe_metrics.apply_labels({"kind": "q_yesno", "answer": "no"}, case)
    assert (accepted["expected_kind"], accepted["expected_answer"]) == ("q_yesno", "no")
    other = probe_metrics.apply_labels({"kind": "q_yesno", "answer": "yes"}, case)
    assert other["expected_kind"] == "guess_wrong"
    unlimited = probe_metrics.apply_labels({"kind": "q_yesno", "answer": "yes"},
                                           {**case, "accept_answers": []})
    assert unlimited["expected_kind"] == "q_yesno"


def test_probe_review_page_controls_and_group_keys(tmp_path):
    results = _review_results()
    out = tmp_path / "probe.html"
    build_probe_page.build_page(results, out)
    summary = out.read_text(encoding="utf-8")
    metrics = probe_metrics.aggregate(results)
    review_data = build_probe_page._review_data(results, metrics)
    assert '<h3 id="human-review">人間チェック後のサマリー</h3>' in summary
    assert f'確認済み 0 / {len(review_data["pairs"])} 組' in summary
    assert 'accept="application/json"' in summary
    assert "window.reviewMetrics = reviewMetrics" in summary
    problem = (out.parent / out.stem / "U01.html").read_text(encoding="utf-8")
    selects = re.findall(r'<select class="review-select" data-pair="([^"]+)"', problem)
    expected = []
    by_id = {case["id"]: case for case in results["cases"]}
    for pattern in results["meta"]["patterns"]:
        for row in results["rows"][pattern["id"]]:
            if row["no"] == "U01" and probe_metrics.row_flags(row, by_id[row["case_id"]])[
                "label_mismatch"]:
                final = row["record"]["final"]
                expected.append(probe_metrics.pair_key(row["case_id"], final["kind"],
                                                       final["answer"]))
    assert selects == expected
    assert f"確認済み 0 / {len(set(expected))} 組" in problem
    assert "未確認の相違だけ" in problem
    assert "../probe.html#human-review" in problem
    for pattern in results["meta"]["patterns"]:
        for row in results["rows"][pattern["id"]]:
            if row["no"] == "U01" and probe_metrics.row_flags(
                    row, by_id[row["case_id"]])["label_mismatch"]:
                assert 'data-sort="✕"' in problem
                break


def test_review_core_matches_python_with_synthetic_results():
    _assert_review_js_matches_python(_review_results())


def test_review_core_matches_full_20261004_results_when_available():
    path = Path(__file__).resolve().parents[1] / "work/probe/full-20261004/results.json"
    if not path.is_file():
        pytest.skip("full-20261004 results.json is not present")
    results = json.loads(path.read_text(encoding="utf-8"))
    assert len(build_probe_page._review_data(results, probe_metrics.aggregate(results))["pairs"]) == 52
    _assert_review_js_matches_python(results)


def test_p1_requires_human_decision_and_shares_reply_key() -> None:
    case = _case("case-1", "impression", no="U01", text="質問")
    first = _row(case, "impression", reply="レントゲンだよ")
    first["record"]["reply"]["guard"] = {
        "words": ["写真"], "original_text": "写真だよ", "original_source": "llm",
    }
    results = {"meta": {"patterns": [{"id": "one"}, {"id": "two"}]},
               "cases": [case], "rows": {"one": [first],
                                           "two": [_row(case, "impression", reply="レントゲンだよ")]}}
    key = probe_metrics.leak_key("case-1", "レントゲンだよ")
    assert key == "leak|case-1|レントゲンだよ"
    baseline = probe_metrics.aggregate(results)
    for pattern in ("one", "two"):
        p1 = baseline["patterns"][pattern]["metrics"]["P1"]
        assert p1["count"] == 0 and p1["candidates_total"] == 1
        assert p1["unconfirmed"] == 1 and p1["pass"] is None
        assert p1["value"] == "確定 0 件（候補 1・未確認 1）"
        assert p1["candidates"][0]["key"] == key
        assert p1["candidates"][0]["decision"] is None
        assert p1["ng"] == []
    guarded = baseline["patterns"]["one"]["reference"]["leak_guard"]
    assert guarded["count"] == 1
    assert guarded["items"] == [{"case_id": "case-1", "no": "U01",
                                 "words": ["写真"], "original_text": "写真だよ"}]

    accepted = probe_metrics.aggregate(results, leak_decisions={key: "not_leak"})
    for pattern in ("one", "two"):
        p1 = accepted["patterns"][pattern]["metrics"]["P1"]
        assert p1["pass"] is True and p1["count"] == 0 and p1["unconfirmed"] == 0
        assert p1["value"] == "確定 0 件（候補 1・未確認 0）"

    rejected = probe_metrics.aggregate(results, leak_decisions={key: "leak"})
    for pattern in ("one", "two"):
        p1 = rejected["patterns"][pattern]["metrics"]["P1"]
        assert p1["pass"] is False and p1["count"] == 1 and p1["unconfirmed"] == 0
        assert p1["value"] == "確定 1 件（候補 1・未確認 0）"
        assert p1["ng"][0]["id"] == "case-1"

    clean = deepcopy(results)
    for rows in clean["rows"].values():
        rows[0]["record"]["reply"]["text"] = "ありがとう"
    empty = probe_metrics.aggregate(clean)["patterns"]["one"]["metrics"]["P1"]
    assert empty["value"] == "0 件" and empty["pass"] is True


def test_p1_default_applies_except_but_explicit_core_keeps_old_check() -> None:
    case = _case("case-u16", "impression", no="U16", text="質問")
    row = _row(case, "impression", reply="遊び方を教えるよ")
    assert probe_metrics.row_flags(row, case)["leak_words"] == []
    assert probe_metrics.row_flags(row, case, {"U16": ["遊び"]})["leak_words"] == ["遊び"]


def test_probe_page_leak_select_escapes_reply_and_key(tmp_path) -> None:
    results = _review_results()
    reply = "レントゲン</SCRIPT><b>"
    for pattern in results["meta"]["patterns"][:2]:
        row = next(row for row in results["rows"][pattern["id"]]
                   if row["case_id"] == "q-yes")
        row["record"]["reply"]["text"] = reply
    report = probe_metrics.aggregate(results)
    data = build_probe_page._review_data(results, report)
    key = probe_metrics.leak_key("q-yes", reply)
    candidates = [item for item in data["leak_candidates"] if item["key"] == key]
    assert len(candidates) == 2
    assert {item["pattern"] for item in candidates} == {
        results["meta"]["patterns"][0]["id"], results["meta"]["patterns"][1]["id"]}
    out = tmp_path / "probe.html"
    build_probe_page.build_page(results, out)
    summary = out.read_text(encoding="utf-8")
    problem = (tmp_path / "probe" / "U01.html").read_text(encoding="utf-8")
    attr = f'data-leak="{build_probe_page._h(key)}"'
    assert summary.count(f'<select class="leak-select" {attr}') == 2
    assert problem.count(f'<select class="leak-select" {attr}') == 2
    assert "漏れ候補: 確認済み 0 / 1" in problem
    assert "漏れ候補: 確認済み 0 / 1" in summary
    assert "漏れ候補 1 件" in summary
    assert "レントゲン&lt;/SCRIPT&gt;&lt;b&gt;" in summary
    assert "レントゲン</SCRIPT><b>" not in summary
    assert "レントゲン\\u003c/SCRIPT>" in summary
    assert "leak_decisions: leaks.map" in summary
    assert "出力ガード発動" in summary
    for decisions in ({}, {key: "not_leak"}, {key: "leak"}):
        _assert_review_js_matches_python(results, decisions)


def test_length_criteria_allow_slack_over_prompt_targets() -> None:
    case = _case("len", "q_yesno", "yes")
    flags = probe_metrics.row_flags(_row(case, "q_yesno", "yes", "はい。" + "あ" * 30), case)
    assert flags["one_liner_over_max"] is False
    flags = probe_metrics.row_flags(_row(case, "q_yesno", "yes", "はい。" + "あ" * 31), case)
    assert flags["one_liner_over_max"] is True
    assert probe_metrics.row_flags(_row(case, "q_yesno", "yes", "あ" * 100),
                                   case)["over_reply_max"] is False
    assert probe_metrics.row_flags(_row(case, "q_yesno", "yes", "あ" * 101),
                                   case)["over_reply_max"] is True
    metrics = _aggregate([case], [_row(case, "q_yesno", "yes", "はい。" + "あ" * 25)])["metrics"]
    assert metrics["L2_one_liner"]["pass"] is True
    assert metrics["L2_one_liner"]["threshold"] == "30 字以内 100%"


def test_conflict_words_count_only_sentence_initial_verdicts() -> None:
    """21-6d17: substrings and restatements are not contradicting verdicts."""
    from tools.probe_metrics import _conflict_words

    assert _conflict_words("いいえ。本当に凍ってはいないよ。", "no") == []
    assert _conflict_words("いいえ。曲名は関係ないよ。", "no") == []
    assert _conflict_words("はい！入ってたよ", "yes") == []
    assert _conflict_words("いいえ。はい、そうだね。", "no") == ["はい"]
    assert _conflict_words("関係ないよ。はい！", "irrelevant") == ["はい"]
    assert _conflict_words("いいえ。関係ありません。", "no") == ["関係ありません"]
    assert _conflict_words("はい！「いいえ」じゃないよ", "yes") == []  # quoted, not a verdict
    assert _conflict_words("はい！いいえ、ちがうかも", "yes") == ["いいえ"]
