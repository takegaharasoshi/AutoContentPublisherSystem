"""Pure aggregation of production-shaped comment reply probe results."""

from __future__ import annotations

import ast
import math
import re
import statistics
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any


SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parents[1]
CORE_PATH = REPO_ROOT / "content/umigame-stock/umigame-soup-1/batch-01/leak_count.py"

from app.judge.contract import KINDS, bare_term_text  # noqa: E402
from app.reply import templates  # noqa: E402


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


@lru_cache(maxsize=4)
def load_core_words(path: Path = CORE_PATH) -> dict[str, list[str]]:
    """Read the literal CORE mapping without executing its script."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == "CORE" for target in targets):
                value = ast.literal_eval(node.value)
                if isinstance(value, dict):
                    return {str(no): list(words) for no, words in value.items()}
    raise ValueError(f"literal CORE mapping not found: {path}")


def answer_matches(row: dict[str, Any]) -> bool:
    """Treat a relevance question's no as equivalent to irrelevant."""
    return row["expected_answer"] == row["answer"] or (
        row["expected_answer"] == "irrelevant" and row["answer"] == "no"
        and any(word in row.get("comment_text", "") for word in RELEVANCE_WORDS)
    )


def apply_labels(row: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Apply alternate acceptable kinds and answers to the expected label."""
    labeled = {**row, "expected_kind": case["expected_kind"],
               "expected_answer": case.get("expected_answer")}
    if row["kind"] in case.get("accept_kinds", []):
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
    core = load_core_words() if core is None else core
    leak_words = [] if not reply or kind == "guess_correct" or reply.startswith("正解") else [
        word for word in core.get(case["no"], [])
        if word and word in reply and word not in case["text"]
    ]
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


def aggregate(results: dict[str, Any]) -> dict[str, Any]:
    """Aggregate each pattern without calls or changes to the input results."""
    cases = {case["id"]: case for case in results["cases"]}
    core = load_core_words()
    output: dict[str, Any] = {"patterns": {}}
    for pattern in results["meta"]["patterns"]:
        pattern_id = pattern["id"]
        items = []
        for row in results["rows"].get(pattern_id, []):
            case = cases[row["case_id"]]
            record = row["record"]
            final = record.get("final") or {}
            reply = (record.get("reply") or {}).get("text")
            flags = row_flags(row, case, core)
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
        leak_items = [{"case_id": x["case"]["id"], "no": x["case"]["no"],
                       "words": x["flags"]["leak_words"], "reply": x["reply"]}
                      for x in items if x["flags"]["leak_words"]]
        phrasing_ng = [x for x in items if x["expected_kind"] in phrasing
                       and phrasing[x["expected_kind"]]["rate"] > .5
                       and (x["reply"] if x["reply"] is not None else "<NO_REPLY>")
                       == phrasing[x["expected_kind"]]["phrase"]]
        ng = {
            "P1": _ng([x for x in items if x["flags"]["leak_words"]],
                      lambda x: "・".join(x["flags"]["leak_words"])),
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
            "P1": _count_metric(len(leak_items), n, "0 件", not leak_items, candidates=leak_items),
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
            "timing": {name: _timing([float(x["row"]["timing"][name]) for x in items
                                      if x["row"]["timing"].get(name) is not None])
                       for name in ("total_s", "judge_s", "writer_s")},
        }
        output["patterns"][pattern_id] = {"metrics": metrics, "reference": reference}
    return output
