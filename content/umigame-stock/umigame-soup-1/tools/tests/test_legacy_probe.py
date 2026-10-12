"""Read archived modes and labels without bringing back their execution paths."""

from __future__ import annotations

from copy import deepcopy
import json

import pytest

from tools import build_probe_page, probe_metrics, probe_sweep


LEGACY_PATTERNS = json.loads('''[
  {"id":"luna-1b","label":"① luna + 1b","judge_mode":"luna","reply_variant":"1b"},
  {"id":"hybrid-1d","label":"③ hybrid + 1d-luna","judge_mode":"hybrid","reply_variant":"1d-luna","shadow":true,"consensus":true},
  {"id":"jev-2b","label":"④ jev + 2b","judge_mode":"jev","reply_variant":"2b"},
  {"id":"dec-2c","label":"⑥ decisions + 2c-luna","judge_mode":"decisions","reply_variant":"2c-luna"},
  {"id":"haiku-1b","label":"⑦ haiku + 1b-haiku","judge_mode":"haiku","reply_variant":"1b-haiku"}
]''')


def _legacy_results() -> dict:
    cases = [
        {"id": "q", "no": "U01", "text": "質問", "expected_kind": "q_yesno", "expected_answer": "yes"},
        {"id": "c", "no": "U01", "text": "正解の推理", "expected_kind": "guess_correct", "expected_answer": None},
        {"id": "w", "no": "U01", "text": "外れた推理", "expected_kind": "guess_wrong", "expected_answer": None},
    ]
    for case in cases:
        case.update(source="eval", accept_kinds=[], accept_answers=[])
    rows = {}
    for pattern in LEGACY_PATTERNS:
        method = pattern["judge_mode"]
        rows[pattern["id"]] = []
        for case in cases:
            judgement = {"kind": case["expected_kind"], "answer": case["expected_answer"], "debug": {}}
            decision = method
            source = "template"
            reply = "はい！" if case["id"] == "q" else "正解！開示文" if case["id"] == "c" else "違うよ。"
            judgements = {method: judgement}
            if method == "hybrid":
                judgements = {"luna": deepcopy(judgement), "jev": deepcopy(judgement)}
                decision = {"q": "luna", "c": "consensus_ok", "w": "consensus_split"}[case["id"]]
                if case["id"] == "w":
                    judgement["kind"] = judgements["luna"]["kind"] = "guess_correct"
                    source, reply = "consensus_split", "もう少し説明してみて。"
            elif method == "decisions":
                judgement["debug"] = {"input_tokens": 100, "output_tokens": 0, "calls": 2,
                                      "refusals": {"count": 1, "names": ["old-stage"]}}
            if case["id"] == "q" and method in {"jev", "decisions", "haiku"}:
                decision = f"{method}_fallback_luna"
                judgements["luna"] = deepcopy(judgement)
                judgement.update(kind=None, answer=None, error="archived failure")
            if method == "jev" and case["id"] != "q":
                judgement["debug"] = {
                    "major": "guess", "probabilities": {
                        "B": {"point_0": {"hit": .9 if case["id"] == "c" else .1, "close": .95}},
                        "B2": .1,
                    },
                }
            rows[pattern["id"]].append({
                "case_id": case["id"], "no": "U01", "record": {
                    "schema_version": 1, "comment_id": case["id"],
                    "config": {"judge_mode": method, "shadow": True, "consensus": True},
                    "judgements": judgements, "shadow_mismatch": method == "hybrid",
                    "final": {"kind": judgement["kind"] if decision == method else (
                        "q_yesno" if case["id"] == "q" else "guess_correct"),
                        "answer": case["expected_answer"], "decision": decision},
                    "reply": {"text": reply, "source": source}, "errors": [],
                }, "timing": {"judge_s": .4, "writer_s": .2, "total_s": .6},
            })
    return {"meta": {"run_at": "2026-10-08T00:00:00Z", "patterns": deepcopy(LEGACY_PATTERNS),
                     "problems": ["U01"], "prompt_version": "archived", "luna_model": "gpt-6-luna",
                     "case_counts": {"U01": {"eval": 3, "bare_term": 0, "common": 0}}},
            "cases": cases, "problems": {"U01": {"problem_text": "過去の問題文"}}, "rows": rows}


def test_archived_json_keeps_decisions_consensus_and_fallbacks_readable(tmp_path) -> None:
    path = tmp_path / "results.json"
    path.write_text(json.dumps(_legacy_results(), ensure_ascii=False), encoding="utf-8")
    before = path.read_bytes()
    results = json.loads(before)
    original = deepcopy(results)
    report = probe_metrics.aggregate(results)
    hybrid = report["patterns"]["hybrid-1d"]
    assert hybrid["reference"]["watch_mismatch"]["count"] == 3
    assert hybrid["reference"]["consensus_split"]["count"] == 1
    assert hybrid["metrics"]["P2"]["count"] == 0
    decisions = report["patterns"]["dec-2c"]["reference"]
    assert decisions["decisions_usage"]["input_tokens"] == 300
    assert decisions["decisions_usage"]["refusals"]["count"] == 3
    for pattern in ("jev-2b", "dec-2c", "haiku-1b"):
        assert report["patterns"][pattern]["reference"]["api_usage"]["judge_fallbacks"] == 1
    page = build_probe_page.build_page(results, tmp_path / "archived.html")
    summary = page.read_text(encoding="utf-8")
    body = (tmp_path / "archived" / "U01.html").read_text(encoding="utf-8")
    assert "5 パターン" in summary and "Decisions" in summary
    for decision in ("consensus_ok", "consensus_split", "decisions_fallback_luna",
                     "jev_fallback_luna", "haiku_fallback_luna"):
        assert build_probe_page.DECISION_LABEL[decision] in body
    assert probe_sweep.STAGED == ("jev",)
    assert probe_sweep.staged_items(results, "jev")
    assert "decisions" in probe_sweep.judgements(results)
    combos = {row["combo"] for row in probe_sweep.consensus(results)}
    assert "luna+jev+haiku+decisions" in combos
    assert results == original and path.read_bytes() == before


@pytest.mark.parametrize("label", ["luna_fallback_haiku", "jev_fallback_haiku", "haiku_fallback_luna",
                                    "jev_fallback_luna", "decisions_fallback_luna"])
def test_fallback_counts_and_page_labels_include_old_and_new(label, tmp_path) -> None:
    results = _legacy_results()
    results["meta"]["patterns"] = results["meta"]["patterns"][:1]
    results["rows"] = {"luna-1b": results["rows"]["luna-1b"]}
    results["rows"]["luna-1b"][0]["record"]["final"]["decision"] = label
    api = probe_metrics.aggregate(results)["patterns"]["luna-1b"]["reference"]["api_usage"]
    assert api["judge_fallbacks"] == 1 and api["fallback_decisions"] == {label: 1}
    build_probe_page.build_page(results, tmp_path / "label.html")
    body = (tmp_path / "label" / "U01.html").read_text(encoding="utf-8")
    assert build_probe_page.DECISION_LABEL[label] in body
