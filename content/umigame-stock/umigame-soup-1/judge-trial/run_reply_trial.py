"""21-6b2 返信文だけを案ごとに試走する CLI。"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
import statistics
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import pattern1_luna
import run_trial
import templates
from judge_contract import HERE, Problem, load_problem


WORK_DIR = HERE / "work"
DEFAULT_SOURCE = WORK_DIR / "trial_results.json"
DEFAULT_VARIANTS = HERE / "reply_variants.json"
RESULTS_PATH = WORK_DIR / "reply_results.json"
REPORT_PATH = WORK_DIR / "reply_report.md"
METRICS_PATH = WORK_DIR / "reply_metrics.json"
COMPARE_PATH = WORK_DIR / "reply_compare.json"
ALLOW_WORDS_PATH = HERE / "prompts" / "reply_allow_words.txt"

ANSWER_WORDS = {
    "yes": ("はい",),
    "no": ("いいえ",),
    "irrelevant": ("関係ありません", "関係ない"),
    "unknown": ("答えに関わりません", "関わらない"),
}
PROXIMITY_WORDS = ("鋭い", "いい線", "近い", "近づ", "核心", "惜しい", "迫っ", "着眼点")
MODEL_PRICES_USD_PER_M = {
    "gpt-6-luna": {"input": 0.10, "output": 0.50},
}

_CJK_OR_KATAKANA = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff々〆ヵヶ]{2,}|[\u30a0-\u30ffー]{2,}")
_EMOJI = re.compile(
    r"(?:[#*0-9]\ufe0f?\u20e3|[\U0001f1e6-\U0001f1ff]{2}|"
    r"[\u2300-\u23ff\u2600-\u27bf\U0001f000-\U0001faff]"
    r"\ufe0f?(?:[\U0001f3fb-\U0001f3ff])?"
    r"(?:\u200d[\u2300-\u23ff\u2600-\u27bf\U0001f000-\U0001faff]"
    r"\ufe0f?(?:[\U0001f3fb-\U0001f3ff])?)*"
    r")"
)
_OPENING_PUNCTUATION = "。．.!！?？、，,:：;；…・ \u3000"
_TEMPLATE_MODULES: dict[str, Any] = {"templates": templates}


def _read_json(path: Path, description: str) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"{description} がありません: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} の JSON が不正です: {exc}") from exc


def load_variants(path: Path) -> list[dict[str, Any]]:
    """案定義を読み、CLI が扱う形を検証する。"""
    data = _read_json(path, "返信案定義")
    if not isinstance(data, list):
        raise ValueError(f"{path} は配列で指定してください")
    variants: list[dict[str, Any]] = []
    names: set[str] = set()
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("返信案はオブジェクトで指定してください")
        name = item.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("返信案には空でない name が必要です")
        if name in names:
            raise ValueError(f"返信案の name が重複しています: {name}")
        names.add(name)
        if item.get("source_method") not in {"p1", "p2"}:
            raise ValueError(f"返信案 {name} の source_method は p1/p2 が必要です")
        variant_type = item.get("type")
        if variant_type not in {"as_is", "template", "llm_fixed"}:
            raise ValueError(f"返信案 {name} の type が不正です: {variant_type}")
        variant = dict(item)
        variant.setdefault("templates_module", "templates")
        if variant_type == "llm_fixed":
            if not isinstance(variant.get("prompt"), str) or not variant["prompt"]:
                raise ValueError(f"返信案 {name} の llm_fixed には prompt が必要です")
            variant.setdefault("model", "gpt-6-luna")
            variant.setdefault("effort", "low")
            variant.setdefault("max_tokens", 800)
            variant.setdefault("with_truth", True)
            if not isinstance(variant["with_truth"], bool):
                raise ValueError(f"返信案 {name} の with_truth は真偽値で指定してください")
            if not isinstance(variant["max_tokens"], int) or variant["max_tokens"] < 1:
                raise ValueError(f"返信案 {name} の max_tokens は 1 以上の整数が必要です")
        variants.append(variant)
    return variants


def load_templates_module(name: str) -> Any:
    """judge-trial 内の定型文モジュールを読み込む。"""
    if name in _TEMPLATE_MODULES:
        return _TEMPLATE_MODULES[name]
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ValueError(f"templates_module はモジュール名で指定してください: {name}")
    path = HERE / f"{name}.py"
    if not path.is_file():
        raise FileNotFoundError(f"templates_module がありません: {path}")
    module_name = f"_reply_trial_{name}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"templates_module を読み込めません: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for attr in ("TEMPLATES", "YESNO_OPENERS", "CORRECT_PREFIX"):
        if not hasattr(module, attr):
            raise ValueError(f"{path} に {attr} がありません")
    _TEMPLATE_MODULES[name] = module
    return module


def _pick_from_module(module: Any, kind: str, comment_id: str) -> str | None:
    options = module.TEMPLATES.get(kind)
    if options is None or len(options) == 0:
        return None
    digest = hashlib.sha1(str(comment_id).encode("utf-8")).digest()
    index = int.from_bytes(digest[:8], "big") % len(options)
    return options[index]


def render_template_reply(
    row: dict[str, Any], problem: Problem, module: Any, comment_id: str | None = None
) -> str | None:
    """既存の SHA-1 選択と判定別テンプレートで返信を組み立てる。"""
    kind = row["kind"]
    case_id = comment_id or row["id"]
    if kind in templates.NO_REPLY_KINDS:
        return None
    if kind == "q_yesno":
        answer = row.get("answer")
        opener = module.YESNO_OPENERS.get(answer, module.YESNO_OPENERS.get("unknown", ""))
        phrase = _pick_from_module(module, "q_yesno", case_id)
        if phrase is None:
            phrase = "次の質問をどうぞ。"
        return opener + phrase
    if kind == "guess_correct":
        return module.CORRECT_PREFIX + problem.reveal_text
    return _pick_from_module(module, kind, case_id)


def _source_error_kind(row: dict[str, Any]) -> str | None:
    if row.get("kind") == "error":
        return "kind_error"
    debug = row.get("debug") if isinstance(row.get("debug"), dict) else {}
    if any(
        row.get(key)
        for key in ("reply_error", "reply_error_message")
    ) or any(debug.get(key) for key in ("error", "reply_error", "reply_error_message")):
        return "reply_error"
    reply = row.get("reply")
    if isinstance(reply, dict) and reply.get("error"):
        return "reply_error"
    return None


def load_source_rows(path: Path, only: list[str] | None = None) -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, dict[str, int]]]:
    """p1/p2 の試走キャッシュ行を読み、失敗行を除外する。"""
    data = _read_json(path, "判定試走キャッシュ")
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("results"), dict):
        raise ValueError(f"{path} の形式が不正です (version=1/results が必要)")
    wanted = set(only or [])
    rows: dict[str, dict[str, dict[str, Any]]] = {"p1": {}, "p2": {}}
    excluded = {"p1": {"kind_error": 0, "reply_error": 0}, "p2": {"kind_error": 0, "reply_error": 0}}
    for key, raw_row in data["results"].items():
        if not isinstance(key, str) or not key.endswith(("::p1", "::p2")):
            continue
        method = key.rsplit("::", 1)[1]
        if not isinstance(raw_row, dict):
            excluded[method]["reply_error"] += 1
            continue
        row = dict(raw_row)
        case_id = str(row.get("id") or key.rsplit("::", 1)[0])
        row["id"] = case_id
        no = str(row.get("no", ""))
        row["no"] = no
        if wanted and no not in wanted:
            continue
        reason = _source_error_kind(row)
        if reason:
            excluded[method][reason] += 1
            continue
        required = ("comment_text", "expected_kind", "kind")
        missing = [field for field in required if field not in row]
        if missing:
            raise ValueError(f"source の {key} に必須項目がありません: {', '.join(missing)}")
        row["method"] = method
        row["comment_text"] = str(row["comment_text"])
        rows[method][case_id] = row
    if only and not any(rows[method] for method in rows):
        raise ValueError(f"--only に一致する有効な source 行がありません: {', '.join(only)}")
    return rows, excluded


def _prompt_path(relative_path: str) -> Path:
    normalized = relative_path.removeprefix("prompts/")
    path = (HERE / "prompts" / normalized).resolve()
    prompt_dir = (HERE / "prompts").resolve()
    try:
        path.relative_to(prompt_dir)
    except ValueError as exc:
        raise ValueError("prompt は prompts/ 配下のファイルで指定してください") from exc
    return path


def _render_prompt(template: str, row: dict[str, Any], problem: Problem, with_truth: bool) -> str:
    truth_values = {
        "truth": problem.truth if with_truth else "",
        "fact_sheet": "\n".join(f"- {fact}" for fact in problem.fact_sheet) if with_truth else "",
        "core_points": "\n".join(f"- {point}" for point in (problem.core_points or problem.truth_points)) if with_truth else "",
    }
    values = {
        "problem_text": problem.problem_text,
        **truth_values,
        "kind": str(row.get("kind") or ""),
        "answer": str(row.get("answer") or ""),
    }
    return re.sub(
        r"\{(problem_text|truth|fact_sheet|core_points|kind|answer)\}",
        lambda match: values[match.group(1)],
        template,
    )


def _call_llm_reply(
    row: dict[str, Any], variant: dict[str, Any], problem: Problem, api_key: str
) -> tuple[str | None, dict[str, Any]]:
    """pattern1_luna のキー取得・再試行実装を使って返信だけを生成する。"""
    started = time.monotonic()
    debug: dict[str, Any] = {
        "input_tokens": 0,
        "output_tokens": 0,
        "latency_s": 0.0,
        "error": None,
    }
    try:
        prompt_path = _prompt_path(variant["prompt"])
        prompt_template = prompt_path.read_text(encoding="utf-8")
        system = _render_prompt(prompt_template, row, problem, variant.get("with_truth", True))
        schema = {
            "type": "object",
            "properties": {"reply": {"type": "string"}},
            "required": ["reply"],
            "additionalProperties": False,
        }
        payload = {
            "model": variant.get("model", "gpt-6-luna"),
            "reasoning_effort": variant.get("effort", "low"),
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": row["comment_text"]},
            ],
            "max_completion_tokens": variant.get("max_tokens", 800),
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "reply_only", "strict": True, "schema": schema},
            },
        }
        req = pattern1_luna.request.Request(
            pattern1_luna.OPENAI_CHAT_COMPLETIONS_URL,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        body = pattern1_luna._post_with_retry(req)
        usage = body.get("usage", {})
        debug["input_tokens"] = int(usage.get("prompt_tokens", 0) or 0)
        debug["output_tokens"] = int(usage.get("completion_tokens", 0) or 0)
        content = body["choices"][0]["message"]["content"]
        decoded = json.loads(content)
        reply = decoded.get("reply") if isinstance(decoded, dict) else None
        if not isinstance(reply, str):
            raise ValueError("JSON reply が文字列ではありません")
        return reply, debug
    except Exception as exc:  # noqa: BLE001 - 1 件の失敗で他の案を止めない
        debug["error"] = str(exc)
        return None, debug
    finally:
        debug["latency_s"] = round(time.monotonic() - started, 6)


def _reply_for_row(
    row: dict[str, Any],
    variant: dict[str, Any],
    problem: Problem,
    module: Any,
    api_key: str | None,
    api_key_error: str | None = None,
) -> tuple[str | None, dict[str, Any]]:
    """案の定義に沿って返信を作り、判定値には触れない。"""
    empty_debug = {"input_tokens": 0, "output_tokens": 0, "latency_s": 0.0, "error": None}
    variant_type = variant["type"]
    if variant_type == "as_is":
        return row.get("reply"), empty_debug
    if variant_type == "template":
        return render_template_reply(row, problem, module), empty_debug
    kind = row["kind"]
    if kind in templates.NO_REPLY_KINDS:
        return None, empty_debug
    if kind in {"troll", "abuse"}:
        return templates.pick(kind, row["id"]), empty_debug
    # llm_correct（真相ありの案だけ）: 本番のパターン 1 と同じく、正解の開示も LLM に書かせる
    llm_writes_correct = variant.get("llm_correct", False) and variant.get("with_truth", True)
    if kind == "guess_correct" and not llm_writes_correct:
        return templates.CORRECT_PREFIX + problem.reveal_text, empty_debug
    if api_key_error:
        return None, {**empty_debug, "error": api_key_error}
    if api_key is None:
        return None, {**empty_debug, "error": "OpenAI API キーがありません"}
    return _call_llm_reply(row, variant, problem, api_key)


def _cache_key(case_id: str, variant_name: str) -> str:
    return f"{case_id}::{variant_name}"


def _load_cache(path: Path = RESULTS_PATH) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    data = _read_json(path, "返信試走キャッシュ")
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("results"), dict):
        raise ValueError(f"{path} の形式が不正です (version=1/results が必要)")
    return data["results"]


def _save_cache(results: dict[str, dict[str, Any]], path: Path = RESULTS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps({"version": 1, "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def _run_job(
    source_row: dict[str, Any], variant: dict[str, Any], problem: Problem, module: Any,
    api_key: str | None, api_key_error: str | None,
) -> dict[str, Any]:
    try:
        reply, debug = _reply_for_row(source_row, variant, problem, module, api_key, api_key_error)
    except Exception as exc:  # noqa: BLE001 - row 単位でエラーを記録
        reply = None
        debug = {"input_tokens": 0, "output_tokens": 0, "latency_s": 0.0, "error": str(exc)}
    return {
        "id": source_row["id"],
        "no": source_row["no"],
        "comment_text": source_row["comment_text"],
        "kind": source_row["kind"],
        "answer": source_row.get("answer"),
        "expected_kind": source_row["expected_kind"],
        "reply": reply,
        "variant": variant["name"],
        "debug": debug,
    }


def _refresh_cached_row(cached: dict[str, Any], source_row: dict[str, Any], variant: dict[str, Any]) -> dict[str, Any]:
    return {
        **cached,
        "id": source_row["id"],
        "no": source_row["no"],
        "comment_text": source_row["comment_text"],
        "kind": source_row["kind"],
        "answer": source_row.get("answer"),
        "expected_kind": source_row["expected_kind"],
        "variant": variant["name"],
    }


def _median_p95_max(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"median": None, "p95": None, "max": None}
    ordered = sorted(values)
    return {
        "median": statistics.median(ordered),
        "p95": ordered[max(0, math.ceil(0.95 * len(ordered)) - 1)],
        "max": max(ordered),
    }


def _one_liner(reply: str | None, openers: list[str]) -> str | None:
    if reply is None:
        return None
    candidates = sorted({opener for opener in openers if opener}, key=len, reverse=True)
    candidates.extend(("はい", "いいえ"))
    for opener in candidates:
        if reply.startswith(opener):
            tail = reply[len(opener):].lstrip(_OPENING_PUNCTUATION)
            return tail.strip()
    return reply.strip()


def _variation(rows: list[dict[str, Any]], *, one_liners: bool = False, openers: list[str] | None = None) -> dict[str, Any]:
    values: list[str] = []
    for row in rows:
        reply = row.get("reply")
        value = _one_liner(reply, openers or []) if one_liners else reply
        values.append("<NO_REPLY>" if value is None else str(value))
    if not values:
        return {"count": 0, "distinct_replies": 0, "most_frequent_reply": None, "most_frequent_count": 0,
                "most_frequent_rate": None, "over_50_percent": False}
    counts = Counter(values)
    most, count = min(counts.items(), key=lambda item: (-item[1], item[0]))
    rate = count / len(values)
    return {
        "count": len(values),
        "distinct_replies": len(counts),
        "most_frequent_reply": most,
        "most_frequent_count": count,
        "most_frequent_rate": rate,
        "over_50_percent": rate > 0.5,
    }


def _load_allow_words(path: Path = ALLOW_WORDS_PATH) -> list[str]:
    if not path.is_file():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _content_words(reply: str) -> list[str]:
    return list(dict.fromkeys(match.group(0) for match in _CJK_OR_KATAKANA.finditer(reply)))


def extract_emojis(reply: str) -> list[str]:
    """返信にある絵文字列を順序を保って重複なく返す。"""
    return list(dict.fromkeys(match.group(0) for match in _EMOJI.finditer(reply)))


def aggregate_variant(
    rows: list[dict[str, Any]],
    variant: dict[str, Any],
    *,
    core: dict[str, list[str]] | None = None,
    allow_words: list[str] | None = None,
    opener_values: list[str] | None = None,
) -> dict[str, Any]:
    """variant 単位の M1〜M7 を計算する。"""
    core = run_trial.load_core_words() if core is None else core
    allow_words = _load_allow_words() if allow_words is None else allow_words
    opener_values = list(opener_values or [])
    opener_values.extend(templates.YESNO_OPENERS.values())

    replies = [row for row in rows if isinstance(row.get("reply"), str)]
    lengths = [len(row["reply"]) for row in replies]
    over_80 = [row for row in replies if len(row["reply"]) > 80]
    by_kind: dict[str, dict[str, Any]] = {}
    kinds = sorted({str(row.get("kind", "")) for row in rows})
    for kind in kinds:
        selected = [row for row in rows if row.get("kind") == kind]
        selected_lengths = [len(row["reply"]) for row in selected if isinstance(row.get("reply"), str)]
        by_kind[kind] = {
            "count": len(selected),
            "reply_count": len(selected_lengths),
            "average_chars": statistics.mean(selected_lengths) if selected_lengths else None,
            "max_chars": max(selected_lengths) if selected_lengths else None,
        }

    yesno = [row for row in rows if row.get("kind") == "q_yesno"]
    one_liners = {row["id"]: _one_liner(row.get("reply"), opener_values) for row in yesno}
    long_one_liners = [
        row for row in yesno
        if one_liners[row["id"]] is not None and len(one_liners[row["id"]]) > 20
    ]
    answer_word_rows = []
    starts_count = 0
    contains_count = 0
    for row in yesno:
        reply = row.get("reply")
        words = ANSWER_WORDS.get(row.get("answer"), ())
        starts = isinstance(reply, str) and any(reply.startswith(word) for word in words)
        contains = isinstance(reply, str) and any(word in reply for word in words)
        starts_count += bool(starts)
        contains_count += bool(contains)
        answer_word_rows.append({"id": row["id"], "answer": row.get("answer"), "words": list(words),
                                 "starts": bool(starts), "contains": bool(contains), "reply": reply})

    core_by_no: dict[str, list[dict[str, Any]]] = defaultdict(list)
    comment_missing_words: list[dict[str, Any]] = []
    for row in rows:
        reply = row.get("reply")
        if not isinstance(reply, str) or not reply:
            continue
        kind = row.get("kind")
        is_disclosure = kind == "guess_correct" or reply.startswith(templates.CORRECT_PREFIX)
        if is_disclosure:
            continue
        no = str(row.get("no", ""))
        comment = str(row.get("comment_text", ""))
        core_words = [word for word in core.get(no, []) if word and word in reply and word not in comment]
        if core_words:
            core_by_no[no].append({"id": row["id"], "words": core_words, "reply": reply})
        if kind in {"q_yesno", "guess_close", "guess_wrong"}:
            candidates = [
                word for word in _content_words(reply)
                if word not in comment
                and not any(word in allowed or allowed in word for allowed in allow_words)
            ]
            if candidates:
                comment_missing_words.append({"id": row["id"], "no": no, "words": candidates, "reply": reply})

    emoji_rows = []
    emoji_counts_by_kind: Counter[str] = Counter()
    all_emoji_types: list[str] = []
    special_emoji_counts: Counter[str] = Counter()
    for row in rows:
        reply = row.get("reply")
        found = extract_emojis(reply) if isinstance(reply, str) else []
        if not found:
            continue
        emoji_counts_by_kind[str(row.get("kind", ""))] += 1
        all_emoji_types.extend(found)
        if row.get("kind") in {"complaint", "abuse", "guess_correct"}:
            special_emoji_counts[str(row["kind"])] += 1
        emoji_rows.append({"id": row["id"], "kind": row.get("kind"), "emojis": found, "reply": reply})

    proximity_rows = []
    for row in rows:
        kind = row.get("kind")
        reply = row.get("reply")
        if kind not in {"q_yesno", "guess_wrong", "guess_close"} or not isinstance(reply, str):
            continue
        words = [word for word in PROXIMITY_WORDS if word in reply]
        if kind == "guess_close":
            words = [word for word in words if word != "惜しい"]
        if words:
            proximity_rows.append({"id": row["id"], "kind": kind, "words": words, "reply": reply})

    metrics: dict[str, Any] = {
        "variant": variant["name"],
        "label": variant.get("label", variant["name"]),
        "rows": len(rows),
        "M1_length": {
            "reply_count": len(lengths),
            "average_chars": statistics.mean(lengths) if lengths else None,
            "max_chars": max(lengths) if lengths else None,
            "over_80_count": len(over_80),
            "over_80_ids": [row["id"] for row in over_80],
            "by_kind": by_kind,
            "q_yesno_one_liner_over_20_count": len(long_one_liners),
            "q_yesno_one_liner_over_20_ids": [row["id"] for row in long_one_liners],
        },
        "M2_answer_word": {
            "q_yesno_count": len(yesno),
            "starts_count": starts_count,
            "starts_rate": starts_count / len(yesno) if yesno else None,
            "contains_count": contains_count,
            "contains_rate": contains_count / len(yesno) if yesno else None,
            "items": answer_word_rows,
        },
        "M3_variation": {
            "by_kind": {kind: _variation([row for row in rows if row.get("kind") == kind]) for kind in kinds},
            "q_yesno_one_liner": _variation(yesno, one_liners=True, openers=opener_values),
            "q_yesno_one_liner_empty_count": sum(value == "" for value in one_liners.values()),
            "q_yesno_one_liner_empty_rate": (
                sum(value == "" for value in one_liners.values()) / len(yesno) if yesno else None
            ),
        },
        "M4_leak_candidates": {
            "core_by_no": {no: {"count": len(items), "items": items} for no, items in sorted(core_by_no.items())},
            "core_count": sum(len(items) for items in core_by_no.values()),
            "comment_missing_content_words_count": len(comment_missing_words),
            "comment_missing_content_words": comment_missing_words,
        },
        "M5_emoji": {
            "reply_count": len(emoji_rows),
            "by_kind": dict(sorted(emoji_counts_by_kind.items())),
            "types": sorted(set(all_emoji_types)),
            "complaint_abuse_guess_correct_count": sum(special_emoji_counts.values()),
            "complaint_abuse_guess_correct_by_kind": dict(sorted(special_emoji_counts.items())),
            "items": emoji_rows,
        },
        "M6_proximity": {"count": len(proximity_rows), "items": proximity_rows},
    }
    if variant.get("type") == "llm_fixed":
        llm_rows = [
            row for row in rows
            if row.get("kind") not in templates.NO_REPLY_KINDS | {"troll", "abuse", "guess_correct"}
        ]
        debug_rows = [row.get("debug") or {} for row in llm_rows]
        input_tokens = sum(int(debug.get("input_tokens", 0) or 0) for debug in debug_rows)
        output_tokens = sum(int(debug.get("output_tokens", 0) or 0) for debug in debug_rows)
        latencies = [float(debug.get("latency_s", 0) or 0) for debug in debug_rows]
        model = variant.get("model", "gpt-6-luna")
        prices = MODEL_PRICES_USD_PER_M.get(model)
        cost = None if prices is None else (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000
        metrics["M7_llm"] = {
            "model": model,
            "request_count": len(llm_rows),
            "latency_s": _median_p95_max(latencies),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost,
            "unit_price_usd_per_million": prices,
            "error_count": sum(bool(debug.get("error")) for debug in debug_rows),
        }
    return metrics


def _report_lines(metrics_by_variant: dict[str, dict[str, Any]], excluded: dict[str, dict[str, int]], source_path: Path) -> list[str]:
    lines = ["# 21-6b2 返信文試走レポート", "", f"入力: `{source_path}`", ""]
    for method, counts in excluded.items():
        total = counts.get("kind_error", 0) + counts.get("reply_error", 0)
        lines.append(f"source {method}: エラー除外 {total} 件 (kind={counts.get('kind_error', 0)}, reply={counts.get('reply_error', 0)})")
    for name, metrics in metrics_by_variant.items():
        m1 = metrics["M1_length"]
        m2 = metrics["M2_answer_word"]
        m3 = metrics["M3_variation"]
        m4 = metrics["M4_leak_candidates"]
        m5 = metrics["M5_emoji"]
        m6 = metrics["M6_proximity"]
        avg = f"{m1['average_chars']:.1f}" if m1["average_chars"] is not None else "対象なし"
        max_chars = m1["max_chars"] if m1["max_chars"] is not None else "対象なし"
        starts_rate = f"{m2['starts_rate']:.1%}" if m2["starts_rate"] is not None else "対象なし"
        contains_rate = f"{m2['contains_rate']:.1%}" if m2["contains_rate"] is not None else "対象なし"
        empty_rate = f"{m3['q_yesno_one_liner_empty_rate']:.1%}" if m3["q_yesno_one_liner_empty_rate"] is not None else "対象なし"
        one_liner_rate = m3["q_yesno_one_liner"]["most_frequent_rate"]
        one_liner_rate_text = f"{one_liner_rate:.1%}" if one_liner_rate is not None else "対象なし"
        one_liner_flag = "50%超" if m3["q_yesno_one_liner"]["over_50_percent"] else "50%以下"
        lines.extend([
            "",
            f"## {name}: {metrics['label']} ({metrics['rows']} 件)",
            f"- M1 字数: 平均 {avg} / 最大 {max_chars} / 80 字超 {m1['over_80_count']} 件 ({', '.join(m1['over_80_ids']) or '該当なし'})",
            f"- M1 q_yesno 一言 20 字超: {m1['q_yesno_one_liner_over_20_count']} 件 ({', '.join(m1['q_yesno_one_liner_over_20_ids']) or '該当なし'})",
            f"- M2 判定語: 冒頭 {m2['starts_count']}/{m2['q_yesno_count']} ({starts_rate}) / 含む {m2['contains_count']}/{m2['q_yesno_count']} ({contains_rate})",
            f"- M3 q_yesno 一言: 異なる {m3['q_yesno_one_liner']['distinct_replies']} 種 / 最頻 {one_liner_rate_text} ({one_liner_flag}) / 判定語のみ {m3['q_yesno_one_liner_empty_count']} 件 ({empty_rate})",
            f"- M4 CORE 語候補 {m4['core_count']} 件 / コメントにない内容語 {m4['comment_missing_content_words_count']} 件",
            f"- M5 絵文字返信 {m5['reply_count']} 件 / 種類 {', '.join(m5['types']) if m5['types'] else 'なし'} / complaint・abuse・guess_correct {m5['complaint_abuse_guess_correct_count']} 件",
            f"- M6 近さを示す語 {m6['count']} 件",
            "- M1 種別ごとの平均 / 最大字数:",
        ])
        for kind, value in m1["by_kind"].items():
            kind_average = f"{value['average_chars']:.1f}" if value["average_chars"] is not None else "対象なし"
            kind_max = value["max_chars"] if value["max_chars"] is not None else "対象なし"
            lines.append(f"  - {kind}: {kind_average} / {kind_max} 字 ({value['reply_count']}/{value['count']} 件に返信)")
        lines.extend([
            "- M3 種別ごとの散らばり:",
        ])
        if metrics["M3_variation"]["by_kind"]:
            for kind, value in metrics["M3_variation"]["by_kind"].items():
                rate = f"{value['most_frequent_rate']:.1%}" if value["most_frequent_rate"] is not None else "対象なし"
                lines.append(f"  - {kind}: {value['count']} 件 / 異なる {value['distinct_replies']} 種 / 最頻 {rate} ({'50%超' if value['over_50_percent'] else '50%以下'})")
        lines.append("- M4 CORE 語候補一覧:")
        if m4["core_by_no"]:
            for no, group in m4["core_by_no"].items():
                for item in group["items"]:
                    lines.append(f"  - {no} / {item['id']} / 語={','.join(item['words'])} / 返信={item['reply']}")
        else:
            lines.append("  - なし")
        lines.append("- M4 コメントにない内容語一覧:")
        if m4["comment_missing_content_words"]:
            for item in m4["comment_missing_content_words"]:
                lines.append(f"  - {item['id']} ({item['no']}) / 語={','.join(item['words'])} / 返信={item['reply']}")
        else:
            lines.append("  - なし")
        lines.append("- M6 近さを示す語一覧:")
        if m6["items"]:
            for item in m6["items"]:
                lines.append(f"  - {item['id']} ({item['kind']}) / 語={','.join(item['words'])} / 返信={item['reply']}")
        else:
            lines.append("  - なし")
        if "M7_llm" in metrics:
            m7 = metrics["M7_llm"]
            latency = m7["latency_s"]
            latency_text = (
                f"{latency['median']:.3f} / {latency['p95']:.3f} / {latency['max']:.3f} 秒"
                if latency["median"] is not None else "対象なし"
            )
            cost_text = f"${m7['cost_usd']:.6f}" if m7["cost_usd"] is not None else "単価未登録"
            lines.append(f"- M7 LLM: 応答時間 中央値/p95/最大 {latency_text} / input {m7['input_tokens']}・output {m7['output_tokens']} tokens / {cost_text} / error {m7['error_count']} 件")
    return lines


def _build_compare(
    source_rows: dict[str, dict[str, dict[str, Any]]],
    variant_rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    cases: dict[str, dict[str, Any]] = {}
    for method, method_rows in source_rows.items():
        for case_id, row in method_rows.items():
            case = cases.setdefault(case_id, {
                "no": row["no"],
                "comment_text": row["comment_text"],
                "kind": {},
                "answer": {},
                "expected_kind": row["expected_kind"],
                "variants": {},
            })
            case["kind"][method] = row["kind"]
            case["answer"][method] = row.get("answer")
    for name, rows in variant_rows.items():
        for row in rows:
            case = cases.setdefault(row["id"], {
                "no": row["no"], "comment_text": row["comment_text"], "kind": {}, "answer": {},
                "expected_kind": row["expected_kind"], "variants": {},
            })
            case["variants"][name] = row.get("reply")
    return {"version": 1, "cases": dict(sorted(cases.items()))}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="21-6b2 判定キャッシュを使って返信文案を試走します")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="run_trial.py の結果キャッシュ")
    parser.add_argument("--variants", nargs="+", help="実行する案名 (省略時は全案)")
    parser.add_argument("--only", nargs="+", metavar="NO", help="対象の問題番号 (例: U01 U13)")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--from-cache", action="store_true", help="返信試走のキャッシュだけで集計")
    parser.add_argument("--force", action="store_true", help="返信試走のキャッシュを無視して作り直す")
    parser.add_argument("--variants-file", type=Path, default=DEFAULT_VARIANTS, help="返信案定義 JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.workers < 1:
        raise SystemExit("--workers は 1 以上を指定してください")
    if args.from_cache and args.force:
        raise SystemExit("--from-cache と --force は同時に指定できません")
    variants = load_variants(args.variants_file)
    available = {variant["name"]: variant for variant in variants}
    selected_names = list(dict.fromkeys(args.variants or [variant["name"] for variant in variants]))
    unknown = [name for name in selected_names if name not in available]
    if unknown:
        raise SystemExit(f"--variants に未定義の案があります: {', '.join(unknown)}")
    selected_variants = [available[name] for name in selected_names]
    source_rows, excluded = load_source_rows(args.source, args.only)
    methods_needed = {variant["source_method"] for variant in selected_variants}
    for method in ("p1", "p2"):
        if method in methods_needed:
            print(f"source {method}: 有効 {len(source_rows[method])} 件 / エラー除外 {sum(excluded[method].values())} 件")

    modules: dict[str, Any] = {}
    for variant in selected_variants:
        module_name = variant.get("templates_module", "templates")
        if variant["type"] == "template" or variant["type"] == "llm_fixed":
            modules[variant["name"]] = load_templates_module(module_name)
        else:
            modules[variant["name"]] = templates

    cache = _load_cache()
    jobs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    keys_by_variant: dict[str, list[str]] = defaultdict(list)
    for variant in selected_variants:
        method = variant["source_method"]
        for row in source_rows[method].values():
            key = _cache_key(row["id"], variant["name"])
            keys_by_variant[variant["name"]].append(key)
            if args.from_cache and key not in cache:
                raise FileNotFoundError(f"--from-cache で必要な返信結果がありません: {key}")
            if args.force or key not in cache:
                jobs.append((row, variant))
            else:
                cache[key] = _refresh_cached_row(cache[key], row, variant)

    needs_problem: set[str] = set()
    needs_llm = False
    for row, variant in jobs:
        kind = row["kind"]
        if variant["type"] == "template" and kind == "guess_correct":
            needs_problem.add(row["no"])
        elif variant["type"] == "llm_fixed":
            if kind == "guess_correct":
                needs_problem.add(row["no"])
            elif kind not in templates.NO_REPLY_KINDS and kind not in {"troll", "abuse"}:
                needs_problem.add(row["no"])
                needs_llm = True
    problems = {no: load_problem(no) for no in sorted(needs_problem)}
    api_key: str | None = None
    api_key_error: str | None = None
    if needs_llm:
        try:
            api_key = pattern1_luna.load_api_key()
        except Exception as exc:  # noqa: BLE001 - API キー不足も各行に記録する
            api_key_error = str(exc)

    if jobs:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(
                    _run_job,
                    row,
                    variant,
                    problems.get(row["no"], Problem(
                        no=row["no"], problem_text=row.get("problem_text", ""), truth="", fact_sheet=[],
                        truth_points=[], reveal_text="", core_points=[]
                    )),
                    modules[variant["name"]],
                    api_key,
                    api_key_error,
                ): (row, variant)
                for row, variant in jobs
            }
            for future in as_completed(futures):
                row, variant = futures[future]
                cache[_cache_key(row["id"], variant["name"])] = future.result()
        _save_cache(cache)
    elif not args.from_cache and not args.force:
        # Preserve a cache file for a valid empty selection and keep the format stable.
        _save_cache(cache)

    variant_rows: dict[str, list[dict[str, Any]]] = {}
    metrics_by_variant: dict[str, dict[str, Any]] = {}
    allow_words = _load_allow_words()
    for variant in selected_variants:
        rows = [cache[key] for key in keys_by_variant[variant["name"]] if key in cache]
        variant_rows[variant["name"]] = rows
        extra_openers: list[str] = []
        module = modules[variant["name"]]
        extra_openers.extend(str(value) for value in module.YESNO_OPENERS.values())
        metrics_by_variant[variant["name"]] = aggregate_variant(
            rows,
            variant,
            core=run_trial.load_core_words(),
            allow_words=allow_words,
            opener_values=extra_openers,
        )

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(_report_lines(metrics_by_variant, excluded, args.source)) + "\n", encoding="utf-8")
    METRICS_PATH.write_text(json.dumps({"version": 1, "variants": metrics_by_variant}, ensure_ascii=False, indent=2), encoding="utf-8")
    COMPARE_PATH.write_text(json.dumps(_build_compare(source_rows, variant_rows), ensure_ascii=False, indent=2), encoding="utf-8")
    for name, metrics in metrics_by_variant.items():
        print(f"{name}: {metrics['rows']} 件 / reply_report.md に集計を出力")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
