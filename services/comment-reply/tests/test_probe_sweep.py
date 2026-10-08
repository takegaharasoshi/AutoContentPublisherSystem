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
