"""Pure aggregation of production-shaped comment reply probe results."""

from __future__ import annotations

import math
import re
import statistics
from collections import Counter
from typing import Any, Mapping


from app.judge.contract import KINDS, bare_term_text  # noqa: E402
from app.reply import leak_guard, templates  # noqa: E402


QUESTION_KINDS = frozenset({"q_yesno", "q_multi", "q_open"})
GUESS_KINDS = frozenset({"guess_correct", "guess_close", "guess_wrong"})
RESTRICTED_KINDS = frozenset({"troll", "abuse", "spam", "personal_info"})
RELEVANCE_WORDS = ("関係", "重要", "大事")
ANSWER_WORDS = {
    "yes": ("はい",), "no": ("いいえ",),
    "irrelevant": ("関係ありません", "関係ない"),
}
OPENERS = tuple(dict.fromkeys((*templates.YESNO_OPENERS.values(),
                                  *(word for words in ANSWER_WORDS.values() for word in words))))
CONFLICT_WORDS = {
    "yes": ("いいえ", "関係ない", "関係ありません"),
    "no": ("はい", "関係ない", "関係ありません"),
    "irrelevant": ("はい", "いいえ"),
}
PROXIMITY_WORDS = ("鋭い", "いい線", "近い", "近づ", "核心", "惜しい", "迫っ", "着眼点")
ALLOWED_EMOJIS = ("☺️", "😌", "😉", "🧐", "🥳", "🙌", "👏", "🤔", "🫢", "🤭", "🤐")
EMOJI = re.compile(
    r"(?:[#*0-9]\ufe0f?\u20e3|[\U0001f1e6-\U0001f1ff]{2}|"
    r"[\u2300-\u23ff\u2600-\u27bf\U0001f000-\U0001faff]"
    r"\ufe0f?(?:[\U0001f3fb-\U0001f3ff])?"
    r"(?:\u200d[\u2190-\u21ff\u2300-\u23ff\u2600-\u27bf\U0001f000-\U0001faff]"
    r"\ufe0f?(?:[\U0001f3fb-\U0001f3ff])?)*"
    r")"
)
OPENING_PUNCTUATION = "。．.!！?？、，,:：;；…・ \u3000"
CORRECT_OPENERS = ("正解です", templates.CORRECT_PREFIX)
PHRASING_MIN_CASES = 20
USD_PER_MILLION = {
    "luna": {"input": 0.10, "output": 0.50},
    "haiku": {"input": 0.10, "output": 0.50},
    "decisions": {"input": 0.10, "output": 0.0},
}
CACHE_READ_MULTIPLIER = 0.1
HAIKU_CACHE_WRITE_MULTIPLIER = 1.25
TOKEN_FIELDS = (
    "input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens",
)


def load_core_words() -> dict[str, list[str]]:
    """Keep the probe's old word-list API backed by the shared dictionary."""
    return {no: list(entry.words) for no, entry in leak_guard.load_leak_words().items()}


def answer_matches(row: dict[str, Any]) -> bool:
    """Treat a relevance question's no as equivalent to irrelevant."""
    return row["expected_answer"] == row["answer"] or (
        row["expected_answer"] == "irrelevant" and row["answer"] == "no"
        and any(word in row.get("comment_text", "") for word in RELEVANCE_WORDS)
    )


def pair_key(case_id: str, kind: str | None, answer: str | None) -> str:
    """人間チェックで同じ判断を共有する行のキーを返す。"""
    return f"{case_id}|{kind or ''}|{answer if kind == 'q_yesno' and answer else ''}"


def leak_key(case_id: str, reply: str) -> str:
    """Share one human leak decision across patterns with the same reply."""
    return f"leak|{case_id}|{reply}"


def apply_labels(row: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Apply alternate acceptable kinds and answers to the expected label."""
    labeled = {**row, "expected_kind": case["expected_kind"],
               "expected_answer": case.get("expected_answer")}
    # 種別 q_yesno を別解にしたケースは、accept_answers があればその答えだけ許容する（21-6d6）
    yesno_limited = (row["kind"] == "q_yesno" and case["expected_kind"] != "q_yesno"
                     and case.get("accept_answers")
                     and row["answer"] not in case["accept_answers"])
    if row["kind"] in case.get("accept_kinds", []) and not yesno_limited:
        labeled["expected_kind"] = row["kind"]
        labeled["expected_answer"] = row["answer"] if row["kind"] == "q_yesno" else None
    if row["kind"] == "q_yesno" and row["answer"] in case.get("accept_answers", []):
        labeled["expected_answer"] = row["answer"]
    return labeled


def _one_liner(reply: str | None) -> str | None:
    if reply is None:
        return None
    for opener in sorted(OPENERS, key=len, reverse=True):
        if reply.startswith(opener):
            return reply[len(opener):].lstrip(OPENING_PUNCTUATION).strip()
    return reply.strip()


def _is_opener(reply: str | None) -> bool:
    return bool(reply and reply.startswith(("はい", "いいえ", "関係", "正解")))


def _emoji_violations(reply: str | None, kind: str | None) -> list[str]:
    found = EMOJI.findall(reply or "")
    problems = [emoji for emoji in found if emoji not in ALLOWED_EMOJIS]
    if len(found) >= 2:
        problems.append("multiple")
    if found and kind in {"complaint", "abuse", "guess_correct"}:
        problems.append("forbidden_kind")
    return problems


def row_flags(row: dict[str, Any], case: dict[str, Any],
              core: dict[str, list[str]] | None = None) -> dict[str, Any]:
    """Return row-level mismatches and reply quality flags."""
    record = row["record"]
    final = record.get("final") or {}
    reply = (record.get("reply") or {}).get("text")
    kind, answer = final.get("kind"), final.get("answer")
    labeled = apply_labels({"kind": kind, "answer": answer,
                            "comment_text": case["text"]}, case)
    kind_mismatch = kind != labeled["expected_kind"]
    answer_mismatch = (kind == "q_yesno" and labeled["expected_kind"] == "q_yesno"
                       and not answer_matches(labeled))
    if not reply or leak_guard.is_correct_reveal(kind, reply):
        leak_words = []
    elif core is not None:
        leak_words = [
            word for word in core.get(case["no"], [])
            if word and word in reply and word not in case["text"]
        ]
    else:
        entry = leak_guard.load_leak_words().get(case["no"])
        leak_words = leak_guard.find_leaks(reply, case["text"], entry) if entry else []
    decision = final.get("decision")
    proximity = [] if decision == "consensus_split" or kind not in {"q_yesno", "guess_wrong"} else [
        word for word in PROXIMITY_WORDS if word in (reply or "")
    ]
    return {
        "kind_mismatch": kind_mismatch, "answer_mismatch": answer_mismatch,
        "label_mismatch": kind_mismatch or answer_mismatch,
        "watch_mismatch": record.get("shadow_mismatch") is True,
        "leak_words": leak_words, "over_80": bool(reply and len(reply) > 80),
        "wrong_correct": labeled["expected_kind"] != "guess_correct" and bool(
            reply and reply.startswith(CORRECT_OPENERS)),
        "opener": bool(reply and (
            any(reply.startswith(word) for word in ANSWER_WORDS.get(answer, ()))
            or reply.startswith(templates.YESNO_OPENERS.get(answer, "\0"))
        )),
        "conflict_words": [word for word in CONFLICT_WORDS.get(answer, ()) if word in (reply or "")]
        if kind == "q_yesno" else [],
        "proximity_words": proximity,
        "emoji_violations": _emoji_violations(reply, kind),
        "one_liner_over_20": bool(
            reply and kind == "q_yesno" and len(_one_liner(reply) or "") > 20
        ),
    }


def _metric(count: int, total: int, threshold: str, passed: bool | None,
            *, rate: float | None = None, value: str | None = None,
            **extra: Any) -> dict[str, Any]:
    if rate is None and total:
        rate = count / total
    if value is None:
        value = f"{rate:.1%}（{count}/{total}）" if rate is not None else "対象なし"
    return {"value": value, "count": count, "total": total, "rate": rate,
            "pass": passed, "threshold": threshold, **extra}


def _count_metric(count: int, total: int, threshold: str, passed: bool | None,
                  **extra: Any) -> dict[str, Any]:
    return _metric(count, total, threshold, passed, value=f"{count} 件", **extra)


def _rate_metric(count: int, total: int, threshold: str, test: Any,
                 **extra: Any) -> dict[str, Any]:
    rate = count / total if total else None
    return _metric(count, total, threshold, test(rate) if rate is not None else None,
                   rate=rate, **extra)


def _ng(selected: list[dict[str, Any]], note: Any = None) -> list[dict[str, str]]:
    """NG になった行の ID 一覧（合否表の折りたたみに出す）。note は行から短い補足を作る関数。"""
    return [{"id": x["case"]["id"], "no": x["case"]["no"],
             "note": note(x) if note else ""} for x in selected]


def _timing(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"median": None, "p95": None, "max": None}
    ordered = sorted(values)
    return {"median": statistics.median(ordered),
            "p95": ordered[math.ceil(0.95 * len(ordered)) - 1], "max": ordered[-1]}


def _accuracy(rows: list[dict[str, Any]]) -> dict[str, Any]:
    count = sum(not row["flags"]["kind_mismatch"] for row in rows)
    return {"count": count, "total": len(rows),
            "rate": count / len(rows) if rows else None}


def present_patterns(results: dict[str, Any]) -> list[dict[str, Any]]:
    """Display only patterns included in the saved results, including legacy runs."""
    return [pattern for pattern in results["meta"]["patterns"]
            if pattern["id"] in results["rows"]]


def _usage_tokens(method: str, debug: dict[str, Any]) -> dict[str, int]:
    """Normalize input totals, including cache tokens, without double billing."""
    usage = debug.get("usage") or {}
    if method == "haiku":
        values = {key: int(usage.get(key, debug.get(key, 0)) or 0) for key in TOKEN_FIELDS}
        values["input_tokens"] += (
            values["cache_read_input_tokens"] + values["cache_creation_input_tokens"]
        )
        return values
    prompt_details = usage.get("prompt_tokens_details") or {}
    return {
        "input_tokens": int(debug.get("prompt_tokens", usage.get("prompt_tokens",
                            debug.get("input_tokens", usage.get("input_tokens", 0)))) or 0),
        "output_tokens": int(debug.get("completion_tokens", usage.get("completion_tokens",
                             debug.get("output_tokens", usage.get("output_tokens", 0)))) or 0),
        "cache_read_input_tokens": int(debug.get("cached_tokens",
                                       prompt_details.get("cached_tokens", 0)) or 0),
        "cache_creation_input_tokens": 0,
    }


def _usage_summary(calls: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    """Sum recorded token costs and failures, keeping refusals separate."""
    totals: dict[str, Any] = {key: 0 for key in TOKEN_FIELDS}
    cost = 0.0
    categories: Counter[str] = Counter()
    empty_reasons: Counter[str] = Counter()
    truncations = 0
    unpriced = set()
    for method, debug in calls:
        tokens = _usage_tokens(method, debug)
        for key in TOKEN_FIELDS:
            totals[key] += tokens[key]
        prices = USD_PER_MILLION.get(method)
        if prices:
            regular_input = max(0, tokens["input_tokens"] - tokens["cache_read_input_tokens"]
                                - tokens["cache_creation_input_tokens"])
            cost += (regular_input * prices["input"] + tokens["output_tokens"] * prices["output"]
                     + tokens["cache_read_input_tokens"] * prices["input"] * CACHE_READ_MULTIPLIER
                     + tokens["cache_creation_input_tokens"] * prices["input"]
                     * HAIKU_CACHE_WRITE_MULTIPLIER) / 1_000_000
        else:
            unpriced.add(method)
        if debug.get("stop_reason") == "refusal":
            categories[debug.get("refusal_category") or "unspecified"] += 1
        else:
            refusals = debug.get("refusals") or {}
            if refusals.get("count"):
                categories["unspecified"] += refusals["count"]
        truncations += (debug.get("stop_reason") == "max_tokens"
                        or debug.get("finish_reason") == "length")
        if debug.get("error_reason") in {"missing_text", "empty_text", "empty_reply"}:
            empty_reasons[debug["error_reason"]] += 1
    return {
        **totals, "cost_usd": round(cost, 10), "unpriced_methods": sorted(unpriced),
        "refusals": {"count": sum(categories.values()), "categories": dict(sorted(categories.items()))},
        "max_tokens": truncations, "empty_responses": sum(empty_reasons.values()),
        "empty_response_reasons": dict(sorted(empty_reasons.items())),
    }


def _api_usage(pattern: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    """Report judge and writer costs, including failed calls and Luna fallbacks."""
    judge_calls = [(method, judgement.get("debug") or {})
                   for item in items
                   for method, judgement in (item["record"].get("judgements") or {}).items()
                   if judgement is not None]
    writer_method = "haiku" if pattern.get("reply_variant") in {"1b-haiku", "1d-haiku"} else "luna"
    writer_calls = [(writer_method, debug) for item in items
                    if (debug := (item["record"].get("reply") or {}).get("debug"))]
    judge, writer = _usage_summary(judge_calls), _usage_summary(writer_calls)
    for name, report in (("judge", judge), ("writer", writer)):
        report["latency_s"] = _timing([
            float(item["row"]["timing"][f"{name}_s"]) for item in items
            if item["row"]["timing"].get(f"{name}_s") is not None
        ])
    categories = Counter(judge["refusals"]["categories"])
    categories.update(writer["refusals"]["categories"])
    return {
        "judge": judge, "writer": writer,
        "cost_usd": round(judge["cost_usd"] + writer["cost_usd"], 10),
        "refusals": {"count": sum(categories.values()), "categories": dict(sorted(categories.items()))},
        "max_tokens": judge["max_tokens"] + writer["max_tokens"],
        "empty_responses": judge["empty_responses"] + writer["empty_responses"],
        "haiku_fallback_luna": sum(
            (item["record"].get("final") or {}).get("decision") == "haiku_fallback_luna"
            for item in items
        ),
    }


def aggregate(results: dict[str, Any],
              accepted: frozenset[str] | set[str] = frozenset(),
              leak_decisions: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Aggregate each pattern without calls or changes to the input results."""
    cases = {case["id"]: case for case in results["cases"]}
    leak_decisions = leak_decisions or {}
    output: dict[str, Any] = {"patterns": {}}
    for pattern in present_patterns(results):
        pattern_id = pattern["id"]
        items = []
        for row in results["rows"].get(pattern_id, []):
            case = cases[row["case_id"]]
            record = row["record"]
            final = record.get("final") or {}
            reply = (record.get("reply") or {}).get("text")
            if pair_key(row["case_id"], final.get("kind"), final.get("answer")) in accepted:
                case = {**case,
                        "accept_kinds": list(dict.fromkeys(
                            [*case.get("accept_kinds", []), final.get("kind")])),
                        "accept_answers": list(dict.fromkeys(
                            [*case.get("accept_answers", []),
                             *([final.get("answer")] if final.get("kind") == "q_yesno"
                               and final.get("answer") else [])]))}
            flags = row_flags(row, case)
            labeled = apply_labels({"kind": final.get("kind"), "answer": final.get("answer"),
                                    "comment_text": case["text"]}, case)
            items.append({"row": row, "case": case, "record": record, "kind": final.get("kind"),
                          "answer": final.get("answer"), "reply": reply, "flags": flags,
                          "expected_kind": labeled["expected_kind"],
                          "expected_answer": labeled["expected_answer"]})
        n = len(items)
        q = [x for x in items if x["expected_kind"] == "q_yesno"]
        p3_cases = [x for x in q if x["expected_answer"] in {"yes", "no"}]
        p3_items = [x for x in p3_cases if x["kind"] == "q_yesno"
                    and x["answer"] in {"yes", "no"} and x["answer"] != x["expected_answer"]]
        by_problem = Counter(x["case"]["no"] for x in p3_items)
        p4_cases = [x for x in q if x["expected_answer"] in {"no", "irrelevant"}]
        p4_items = [x for x in p4_cases if x["kind"] == "q_yesno"
                    and x["answer"] in {"no", "irrelevant"}
                    and not answer_matches({"expected_answer": x["expected_answer"],
                                            "answer": x["answer"],
                                            "comment_text": x["case"]["text"]})]
        correct = [x for x in items if x["expected_kind"] == "guess_correct"]
        undeclared = [x for x in correct
                      if not (x["reply"] and x["reply"].startswith(CORRECT_OPENERS))]
        declared = len(correct) - len(undeclared)
        restricted = [x for x in items if x["expected_kind"] in RESTRICTED_KINDS]
        troll_abuse = [x for x in items if x["expected_kind"] in {"troll", "abuse"}]
        no_reply = [x for x in items if x["expected_kind"] in templates.NO_REPLY_KINDS]
        ordinary = [x for x in items if x["expected_kind"] not in RESTRICTED_KINDS]
        p6_ng = (
            _ng([x for x in restricted if _is_opener(x["reply"])], lambda x: "⑱〜㉑ に判定語")
            + _ng([x for x in troll_abuse
                   if x["reply"] != templates.pick(x["expected_kind"], x["case"]["id"])],
                  lambda x: "⑱⑲ が定型文でない")
            + _ng([x for x in no_reply if x["reply"]], lambda x: "⑳㉑ に返信")
            + _ng([x for x in ordinary if x["kind"] in RESTRICTED_KINDS],
                  lambda x: f"普通のコメントを {x['kind']} と判定")
        )
        p6_counts = {
            "restricted_openers": sum(_is_opener(x["reply"]) for x in restricted),
            "template": sum(x["reply"] == templates.pick(x["expected_kind"], x["case"]["id"])
                            for x in troll_abuse),
            "no_reply_violation": sum(bool(x["reply"]) for x in no_reply),
            "ordinary_restricted": sum(x["kind"] in RESTRICTED_KINDS for x in ordinary),
        }
        template_rate = p6_counts["template"] / len(troll_abuse) if troll_abuse else None
        ordinary_rate = p6_counts["ordinary_restricted"] / len(ordinary) if ordinary else None
        p6_pass = (p6_counts["restricted_openers"] == 0 and
                   (template_rate is None or template_rate >= .8) and
                   p6_counts["no_reply_violation"] == 0 and
                   (ordinary_rate is None or ordinary_rate <= .05))
        by_kind = {kind: _accuracy([x for x in items if x["expected_kind"] == kind])
                   for kind in KINDS}
        groups = {
            "質問系 ①〜③": _accuracy([x for x in items if x["expected_kind"] in QUESTION_KINDS]),
            "推理系 ④〜⑥": _accuracy([x for x in items if x["expected_kind"] in GUESS_KINDS]),
            "その他 ⑦〜㉒": _accuracy([
                x for x in items
                if x["expected_kind"] not in QUESTION_KINDS | GUESS_KINDS
            ]),
        }
        kind_accuracy = _accuracy(items)
        low_kinds = {kind: entry for kind, entry in by_kind.items()
                     if kind not in QUESTION_KINDS and entry["rate"] is not None and entry["rate"] < .8}
        non_question_rates = [entry["rate"] for kind, entry in by_kind.items()
                              if kind not in QUESTION_KINDS and entry["rate"] is not None]
        # 5.1.1 L1②: 同じ種別の返事 20 件のうちの最頻。返信しない種別と開示文が 1 つに決まる ④ は数えない
        phrasing = {}
        for kind in KINDS:
            if kind in templates.NO_REPLY_KINDS or kind == "guess_correct":
                continue
            selected = [x for x in items if x["expected_kind"] == kind]
            if len(selected) >= PHRASING_MIN_CASES:
                counts = Counter(x["reply"] if x["reply"] is not None else "<NO_REPLY>"
                                 for x in selected)
                phrase, count = min(counts.items(), key=lambda item: (-item[1], item[0]))
                phrasing[kind] = {"phrase": phrase, "count": count,
                                  "total": len(selected), "rate": count / len(selected)}
        guidance = [x for x in items if x["expected_kind"] in {"q_multi", "q_open"}]
        unguided = [x for x in guidance
                    if not (x["kind"] in {"q_multi", "q_open"} and bool(x["reply"]))]
        guided = len(guidance) - len(unguided)
        final_yesno = [x for x in items if x["kind"] == "q_yesno"]
        opener_rows = [x for x in final_yesno
                       if (x["record"].get("final") or {}).get("decision") != "consensus_split"]
        one_liner_count = sum(bool(x["reply"]) and not x["flags"]["one_liner_over_20"]
                              for x in final_yesno)
        opener_count = sum(x["flags"]["opener"] for x in opener_rows)
        split_accuracy = {}
        for name, is_new in (("existing", False), ("new", True)):
            selected = [x for x in q if ("-b" in x["case"]["id"]) == is_new]
            matched = sum(x["kind"] == "q_yesno" and not x["flags"]["answer_mismatch"]
                          for x in selected)
            split_accuracy[name] = _rate_metric(matched, len(selected), "参考", lambda _: None)
        bare = [x for x in items if x["case"]["source"] == "bare_term"]
        bare_count = sum(x["kind"] == "q_open" and bool(x["reply"])
                         and bare_term_text(x["case"]["text"]) in x["reply"] for x in bare)
        leak_items = []
        for x in items:
            words = x["flags"]["leak_words"]
            if not words:
                continue
            key = leak_key(x["case"]["id"], x["reply"])
            decision = leak_decisions.get(key)
            leak_items.append({
                "case_id": x["case"]["id"], "no": x["case"]["no"],
                "words": words, "reply": x["reply"], "key": key,
                "decision": decision if decision in {"leak", "not_leak"} else None,
            })
        confirmed_leaks = [x for x in leak_items if x["decision"] == "leak"]
        unconfirmed_leaks = sum(x["decision"] is None for x in leak_items)
        guard_items = [{"case_id": x["case"]["id"], "no": x["case"]["no"],
                        "words": guard["words"], "original_text": guard["original_text"]}
                       for x in items
                       if (guard := (x["record"].get("reply") or {}).get("guard"))]
        phrasing_ng = [x for x in items if x["expected_kind"] in phrasing
                       and phrasing[x["expected_kind"]]["rate"] > .5
                       and (x["reply"] if x["reply"] is not None else "<NO_REPLY>")
                       == phrasing[x["expected_kind"]]["phrase"]]
        ng = {
            "P1": [{"id": x["case_id"], "no": x["no"],
                    "note": "・".join(x["words"])} for x in confirmed_leaks],
            "P2": _ng([x for x in items if x["flags"]["wrong_correct"]]),
            "P3": _ng(p3_items, lambda x: f"{x['expected_answer']} → {x['answer']}"),
            "P4": _ng(p4_items, lambda x: f"{x['expected_answer']} → {x['answer']}"),
            "P5": _ng(undeclared, lambda x: f"判定 {x['kind']}"),
            "P6": p6_ng,
            "P7": _ng([x for x in items if x["flags"]["over_80"]],
                      lambda x: f"{len(x['reply'])} 字"),
            "L1_kind": _ng([x for x in items if x["flags"]["kind_mismatch"]],
                           lambda x: f"{x['expected_kind']} → {x['kind']}"),
            "L1_kind_each": _ng([x for x in items if x["flags"]["kind_mismatch"]
                                 and x["expected_kind"] in low_kinds],
                                lambda x: f"{x['expected_kind']} → {x['kind']}"),
            "L1_phrasing": _ng(phrasing_ng, lambda x: f"最頻の言い回し（{x['expected_kind']}）"),
            "L1_guidance": _ng(unguided, lambda x: f"判定 {x['kind']}"),
            "L2_one_liner": _ng([x for x in final_yesno
                                 if not x["reply"] or x["flags"]["one_liner_over_20"]],
                                lambda x: f"一言 {len(_one_liner(x['reply']) or '')} 字"),
            "L2_opener": _ng([x for x in opener_rows if not x["flags"]["opener"]],
                             lambda x: f"判定 {x['answer']}"),
            "L2_conflict": _ng([x for x in final_yesno if x["flags"]["conflict_words"]],
                               lambda x: "・".join(x["flags"]["conflict_words"])),
            "L2_proximity": _ng([x for x in items if x["flags"]["proximity_words"]],
                                lambda x: "・".join(x["flags"]["proximity_words"])),
            "L2_emoji": _ng([x for x in items if x["flags"]["emoji_violations"]],
                            lambda x: "・".join(x["flags"]["emoji_violations"])),
        }
        metrics = {
            "P1": _metric(
                len(confirmed_leaks), n, "0 件",
                False if confirmed_leaks else None if unconfirmed_leaks else True,
                value=(f"確定 {len(confirmed_leaks)} 件（候補 {len(leak_items)}・"
                       f"未確認 {unconfirmed_leaks}）" if leak_items else "0 件"),
                candidates=leak_items, candidates_total=len(leak_items),
                unconfirmed=unconfirmed_leaks,
            ),
            "P2": _count_metric(sum(x["flags"]["wrong_correct"] for x in items), n, "0 件",
                                not any(x["flags"]["wrong_correct"] for x in items)),
            "P3": _metric(len(p3_items), len(p3_cases), "全質問の 3% 以下・1 問 2 件以下",
                          (len(p3_items) <= .03 * len(p3_cases)
                           and max(by_problem.values(), default=0) <= 2) if p3_cases else None,
                          rate=len(p3_items) / len(p3_cases) if p3_cases else None,
                          value=f"{len(p3_items)} 件 / {len(p3_cases)} 件",
                          by_problem=dict(sorted(by_problem.items()))),
            "P4": _rate_metric(len(p4_items), len(p4_cases), "10% 以下", lambda rate: rate <= .1),
            "P5": _rate_metric(declared, len(correct), "80% 以上", lambda rate: rate >= .8),
            "P6": _metric(sum((p6_counts["restricted_openers"], p6_counts["no_reply_violation"],
                               p6_counts["ordinary_restricted"])), n,
                          "⑱〜㉑ 判定語 0・⑱⑲ 定型 80% 以上・⑳㉑ 返信 0・普通→不適切 5% 以下",
                          p6_pass, rate=None,
                          value=(f"{p6_counts['restricted_openers']} 件 / "
                                 f"{template_rate:.1%}" if template_rate is not None else
                                 f"{p6_counts['restricted_openers']} 件 / 対象なし")
                          + f" / {p6_counts['no_reply_violation']} 件 / "
                          + (f"{ordinary_rate:.1%}" if ordinary_rate is not None else "対象なし"),
                          details={**p6_counts, "template_total": len(troll_abuse),
                                   "template_rate": template_rate, "ordinary_total": len(ordinary),
                                   "ordinary_rate": ordinary_rate}),
            "P7": _count_metric(sum(x["flags"]["over_80"] for x in items), n, "0 件",
                                not any(x["flags"]["over_80"] for x in items)),
            "L1_kind": _metric(kind_accuracy["count"], n, "全体 90% 以上",
                               kind_accuracy["rate"] >= .9
                               if kind_accuracy["rate"] is not None else None,
                               rate=kind_accuracy["rate"], by_kind=by_kind, groups=groups),
            # 10.2 L1① の後段。全体とは別の行にして、どの種別で落ちたかを見えるようにする
            "L1_kind_each": _metric(
                len(low_kinds), len(non_question_rates), "質問以外の各種別 80% 以上",
                not low_kinds if non_question_rates else None,
                rate=min(non_question_rates, default=None),
                value=("・".join(f"{kind} {entry['rate']:.1%}（{entry['count']}/{entry['total']}）"
                                for kind, entry in low_kinds.items())
                       if low_kinds else
                       f"最低 {min(non_question_rates):.1%}" if non_question_rates else "対象なし"),
                by_kind=low_kinds,
                # 合否表で種別ごとに 1 行ずつ出すための内訳（NG の ID 付き）
                kinds={kind: {**entry,
                              "pass": entry["rate"] >= .8 if entry["rate"] is not None else None,
                              "ng": _ng([x for x in items if x["flags"]["kind_mismatch"]
                                         and x["expected_kind"] == kind],
                                        lambda x: f"{x['expected_kind']} → {x['kind']}")}
                       for kind, entry in by_kind.items() if kind not in QUESTION_KINDS}),
            "L1_phrasing": _metric(
                max((v["count"] for v in phrasing.values()), default=0),
                max((v["total"] for v in phrasing.values()), default=0),
                "20 件以上の各種別で 50% 以下",
                all(v["rate"] <= .5 for v in phrasing.values()) if phrasing else None,
                rate=max((v["rate"] for v in phrasing.values()), default=None),
                value=(f"最大 {max(v['rate'] for v in phrasing.values()):.1%}"
                       if phrasing else "対象なし"),
                by_kind=phrasing,
            ),
            "L1_guidance": _rate_metric(guided, len(guidance), "80% 以上", lambda rate: rate >= .8),
            "L2_one_liner": _rate_metric(one_liner_count, len(final_yesno), "20 字以内 100%",
                                          lambda rate: rate == 1),
            "L2_opener": _rate_metric(opener_count, len(opener_rows), "判定語始まり 100%",
                                       lambda rate: rate == 1),
            "L2_conflict": _count_metric(
                sum(bool(x["flags"]["conflict_words"]) for x in final_yesno),
                len(final_yesno), "0 件",
                not any(x["flags"]["conflict_words"] for x in final_yesno),
            ),
            "L2_proximity": _count_metric(sum(bool(x["flags"]["proximity_words"]) for x in items),
                                           n, "0 件",
                                           not any(x["flags"]["proximity_words"] for x in items)),
            "L2_emoji": _count_metric(sum(bool(x["flags"]["emoji_violations"]) for x in items),
                                       n, "0 件",
                                       not any(x["flags"]["emoji_violations"] for x in items)),
        }
        for key, entries in ng.items():
            metrics[key]["ng"] = entries
        reference = {
            "api_usage": _api_usage(pattern, items),
            "yesno_accuracy": split_accuracy,
            "bare_term": _rate_metric(bare_count, len(bare), "参考", lambda _: None),
            "watch_mismatch": _count_metric(sum(x["flags"]["watch_mismatch"] for x in items), n,
                                             "参考", None),
            "consensus_split": _count_metric(
                sum((x["record"].get("final") or {}).get("decision") == "consensus_split"
                    for x in items), n, "参考", None,
            ),
            "errors": _count_metric(
                sum(bool(x["record"].get("errors")) for x in items), n, "参考", None,
            ),
            "fallback": _count_metric(sum((x["record"].get("reply") or {}).get("source")
                                         == "fallback_template" for x in items), n, "参考", None),
            "leak_guard": _count_metric(len(guard_items), n, "参考", None,
                                         items=guard_items),
            "timing": {name: _timing([float(x["row"]["timing"][name]) for x in items
                                      if x["row"]["timing"].get(name) is not None])
                       for name in ("total_s", "judge_s", "writer_s")},
        }
        if pattern.get("judge_mode") == "decisions":
            debug_items = [(x["record"].get("judgements", {}).get("decisions") or {}).get(
                "debug", {}
            ) for x in items]
            reference["decisions_usage"] = {
                key: sum(debug.get(key, 0) for debug in debug_items)
                for key in ("input_tokens", "output_tokens", "calls")
            }
            reference["decisions_usage"]["refusals"] = {
                "count": sum(debug.get("refusals", {}).get("count", 0) for debug in debug_items),
                "names": [name for debug in debug_items
                          for name in debug.get("refusals", {}).get("names", [])],
            }
        output["patterns"][pattern_id] = {"metrics": metrics, "reference": reference}
    return output
