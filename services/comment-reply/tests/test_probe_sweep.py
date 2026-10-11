"""Offline checks for the stage-B threshold sweep and consensus estimate (21-6d11)."""

from __future__ import annotations

import json
from pathlib import Path

from tools import probe_sweep


def _judgement(kind: str, points: dict | None = None, b2: float | None = None,
               major: str = "guess") -> dict:
    probabilities: dict = {}
    if points is not None:
        probabilities["B"] = points
    if b2 is not None:
        probabilities["B2"] = b2
    return {"kind": kind, "debug": {"major": major, "probabilities": probabilities}}


def _results() -> dict:
    cases = [
        {"id": "c1", "no": "U01", "text": "正解の推理", "expected_kind": "guess_correct"},
        {"id": "c2", "no": "U01", "text": "惜しい推理", "expected_kind": "guess_close"},
        {"id": "c3", "no": "U01", "text": "外れの推理", "expected_kind": "guess_wrong"},
        {"id": "c4", "no": "U01", "text": "別解で正解", "expected_kind": "guess_close",
         "accept_kinds": ["guess_correct"]},
    ]
    jev = {
        "c1": _judgement("guess_correct", {"p1": {"hit": 0.9, "close": 1.0}}, 0.1),
        "c2": _judgement("guess_close", {"p1": {"hit": 0.4, "close": 0.9}}),
        "c3": _judgement("guess_wrong", {"p1": {"hit": 0.0, "close": 0.2}}),
        "c4": _judgement("guess_correct", {"p1": {"hit": 0.6, "close": 0.9}}, 0.2),
    }
    luna = {"c1": {"kind": "guess_correct"}, "c2": {"kind": "guess_correct"},
            "c3": {"kind": "guess_wrong"}, "c4": {"kind": "guess_close"}}

    def rows(method: str, found: dict) -> list:
        return [{"case_id": case_id, "record": {"judgements": {method: judgement}}}
                for case_id, judgement in found.items()]

    return {"cases": cases, "rows": {"luna-1b": rows("luna", luna), "jev-2b": rows("jev", jev)}}


def test_point_sweep_marks_missing_b2_and_accepts_alternate_correct() -> None:
    items = probe_sweep.staged_items(_results(), "jev")
    table = {row["t_point"]: row for row in probe_sweep.point_sweep(items, 1)}
    # 0.5: c1・c4 が宣言。c4 は別解で ④ を許容しているので誤りに数えない
    assert table[0.5]["wrong_correct"] == 0 and table[0.5]["true_declared"] == 1
    # 0.3: c2 が候補に入るが段 B2 を呼んでいない
    assert table[0.3]["b2_missing"] == 1
    assert table[0.9]["true_declared"] == 1 and table[0.9]["p5"] == 1.0


def test_close_sweep_splits_guess_path() -> None:
    items = probe_sweep.staged_items(_results(), "jev")
    table = {row["t_close"]: row for row in probe_sweep.close_sweep(items)}
    assert table[0.25] == {"t_close": 0.25, "pool": 2, "close_label_close": 1,
                           "close_as_wrong": 0, "wrong_as_close": 0,
                           "label_close": 1, "label_wrong": 1}
    assert table[0.15]["wrong_as_close"] == 1


def test_consensus_requires_every_method() -> None:
    table = {row["combo"]: row for row in probe_sweep.consensus(_results())}
    assert table["luna"]["wrong_correct"] == 1  # c2 を luna が ④ にした
    assert table["luna+jev"]["wrong_correct"] == 0
    assert table["luna+jev"]["true_declared"] == 1
    assert table["luna+jev"]["split"] == 2  # c2（luna だけ）・c4（jev だけ）
    assert "decisions" not in table and "haiku" not in table


def test_main_writes_report_without_api(tmp_path: Path, capsys) -> None:
    (tmp_path / "results.json").write_text(json.dumps(_results()), encoding="utf-8")
    assert probe_sweep.main(["--probe", str(tmp_path)]) == 0
    report = json.loads((tmp_path / "sweep.json").read_text(encoding="utf-8"))
    assert report["total_correct"] == 1 and "jev" in report and "decisions" not in report
    assert "合意ルール" in capsys.readouterr().out


def test_sweep_reads_any_jev_pattern_and_new_default_single_pass_patterns(tmp_path) -> None:
    from copy import deepcopy

    original = _results()
    expected = probe_sweep.staged_items(original, "jev")
    for pattern in ("jev-2b", "jev-2c", "jev-1b-haiku"):
        results = deepcopy(original)
        results["rows"][pattern] = results["rows"].pop("jev-2b")
        results["rows"]["luna-1b-haiku"] = results["rows"].pop("luna-1b")
        results["rows"]["haiku-1b-high"] = [{
            "case_id": "c1", "record": {"judgements": {"haiku": {"kind": "guess_correct"}}},
        }]
        assert probe_sweep.staged_items(results, "jev") == expected
        found = probe_sweep.judgements(results)
        assert found["luna"]["c1"]["kind"] == found["haiku"]["c1"]["kind"] == "guess_correct"
        (tmp_path / "results.json").write_text(json.dumps(results), encoding="utf-8")
        assert probe_sweep.main(["--probe", str(tmp_path)]) == 0
        report = json.loads((tmp_path / "sweep.json").read_text())
        assert "jev" in report and "decisions" not in report


def test_fill_b2_uses_only_jev(tmp_path, monkeypatch) -> None:
    from unittest.mock import Mock
    from app.judge import jev

    monkeypatch.setenv("TYPESAFE_API_KEY", "fake-jev")
    call = Mock(return_value={"contradict": {"noul": {"true": .7}}})
    monkeypatch.setattr(jev, "_record_call", call)
    items = [{"id": "b2", "no": "U01", "text": "推理", "b2": None,
              "points": {"p": {"hit": .4, "close": .6}}}]
    cache = {}
    probe_sweep.fill_b2(items, cache, workers=1)
    assert items[0]["b2"] == cache["b2"] == .7
    assert call.call_args.args[0] == "fake-jev"
    probe_sweep.fill_b2(items, cache, workers=1)
    call.assert_called_once()


def test_older_threshold_run_keeps_recorded_question_path() -> None:
    results = _results()
    judgement = results["rows"]["jev-2b"][0]["record"]["judgements"]["jev"]
    judgement["kind"] = "guess_close"
    judgement["debug"].update(major="question", probabilities={
        "B": {"p1": {"hit": .55, "close": .8}}, "B2": .7,
    })
    item = probe_sweep.staged_items(results, "jev")[0]
    assert item["path"] == "q_yesno"
    judgement["debug"]["guess_demoted"] = True
    assert probe_sweep.staged_items(results, "jev")[0]["path"] == "guess"
