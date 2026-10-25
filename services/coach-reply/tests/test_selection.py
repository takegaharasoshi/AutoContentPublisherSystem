"""Exclusion order and conservative first-place behavior."""

from __future__ import annotations

from copy import deepcopy

import pytest

from app.first_correct import is_first_correct
from app.reply_text import CORRECT, FIRST_CORRECT, make_reply
from app.selection import select_comments
from app.switch import parse_utc_timestamp


START = parse_utc_timestamp("2026-10-24T01:00:00Z")


def comment(cid: str, minute: int = 1, **kwargs) -> dict:
    return {
        "id": cid, "text": "答え", "username": "reader",
        "timestamp": f"2026-10-24T01:{minute:02}:00Z", **kwargs,
    }


def test_selection_joins_reply_ids_and_own_rows_before_filtering() -> None:
    comments = [
        comment("candidate"),
        comment("manual", replies={"data": [{"id": "own-reply"}]}),
        comment("own-reply", username="coach"),
        comment("thread", replies={"data": [{"id": "reader-reply"}]}),
        comment("reader-reply"),
        comment("own-post", username="coach"),
        comment("old", timestamp="2026-10-24T00:59:59Z"),
        comment("judged"),
        {"id": "no-body", "timestamp": "2026-10-24T00:00:00Z"},
        comment("blank", text=" \n"),
        comment("retry"),
        comment("candidate"),
    ]
    saved = {"judged": {"verdict": "wrong"}, "retry": {"fail_count": 1}}
    original = deepcopy((comments, saved))
    selected = select_comments(comments, "coach", saved, START)
    assert [c["id"] for c in selected.candidates] == ["candidate", "thread", "retry"]
    assert [c["id"] for c in selected.operator_replied] == ["manual"]
    assert [c["id"] for c in selected.before_start] == ["old"]
    assert [c["id"] for c in selected.already_judged] == ["judged"]
    assert selected.has_operator_reply
    assert "no-body" in {c["id"] for c in selected.top_level}
    assert {"own-post", "own-reply", "reader-reply"}.isdisjoint(c["id"] for c in selected.top_level)
    assert (comments, saved) == original


def test_already_judged_precedes_operator_reply_and_start_boundary_is_inclusive() -> None:
    comments = [
        comment("saved", replies={"data": [{"id": "r"}]}),
        comment("r", username="coach"),
        comment("boundary", timestamp="2026-10-24T01:00:00+0000"),
    ]
    selected = select_comments(comments, "coach", {"saved": {"verdict": "correct"}}, START)
    assert [c["id"] for c in selected.already_judged] == ["saved"]
    assert not selected.operator_replied
    assert [c["id"] for c in selected.candidates] == ["boundary"]


def test_empty_comments_and_unrelated_own_row() -> None:
    assert not select_comments([], "coach", {}, START).has_operator_reply
    assert not select_comments([comment("own", username="coach")], "coach", {}, START).has_operator_reply


def test_invalid_comment_timestamp_cannot_be_judged() -> None:
    with pytest.raises(ValueError):
        select_comments([comment("c", timestamp="invalid")], "coach", {}, START)


@pytest.mark.parametrize("verdict", ["correct", "alt", "unsure", "before_start", "operator_replied", "judge_failed", None])
def test_first_place_blocked_by_any_earlier_non_wrong_or_unjudged(verdict) -> None:
    previous, current = comment("earlier", 1), comment("current", 2)
    records = {"current": {"verdict": "correct", "confidence": "high"}}
    if verdict:
        records["earlier"] = {"verdict": verdict}
    assert not is_first_correct(current, [previous, current], records,
                                first_correct_replied=False, has_operator_reply=False)


@pytest.mark.parametrize("earlier", [[], [comment("earlier", 1)]])
def test_first_place_allowed_only_with_no_earlier_answers_or_all_wrong(earlier) -> None:
    current = comment("current", 2)
    records = {"current": {"verdict": "correct", "confidence": "high"},
               "earlier": {"verdict": "wrong"}}
    assert is_first_correct(current, [*earlier, current, comment("later", 3)], records,
                            first_correct_replied=False, has_operator_reply=False)


@pytest.mark.parametrize("flag", ["first_correct_replied", "has_operator_reply"])
def test_first_place_post_flags_block_claim(flag) -> None:
    current = comment("c")
    flags = {"first_correct_replied": False, "has_operator_reply": False, flag: True}
    assert not is_first_correct(current, [current], {"c": {"verdict": "correct", "confidence": "high"}}, **flags)


def test_first_place_unknown_earlier_timestamp_and_low_confidence_block_claim() -> None:
    current = comment("c", 2)
    records = {"c": {"verdict": "correct", "confidence": "high"}}
    assert not is_first_correct(current, [{"id": "no-time"}, current], records,
                                first_correct_replied=False, has_operator_reply=False)
    records["c"]["confidence"] = "low"
    assert not is_first_correct(current, [current], records,
                                first_correct_replied=False, has_operator_reply=False)


@pytest.mark.parametrize("first,pool", [(False, CORRECT), (True, FIRST_CORRECT)])
def test_fixed_reply_candidates_and_injectable_random(first, pool) -> None:
    seen = []

    def choose(options):
        seen.append(options)
        return options[-1]

    assert make_reply("reader", first=first, chooser=choose) == f"@reader {pool[-1]}"
    assert seen == [pool]
    assert len(CORRECT) == 16
    assert len(FIRST_CORRECT) == 6


def test_reply_requires_recipient() -> None:
    with pytest.raises(ValueError):
        make_reply("")
