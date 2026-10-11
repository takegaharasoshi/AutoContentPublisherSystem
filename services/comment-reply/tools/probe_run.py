"""Run evaluation cases through the production combiner, writer and comment log."""

from __future__ import annotations

import argparse
import builtins
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable


SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parents[1]
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from app.comment_log import apply_decision, new_record, prompt_version, utc_now  # noqa: E402
from app import anthropic_util  # noqa: E402
from app.config import Config  # noqa: E402
from app.judge import haiku, jev, luna  # noqa: E402
from app.judge.combiner import Combined, combine  # noqa: E402
from app.judge.contract import ANSWERS, Judgement, KINDS, Problem  # noqa: E402
from app.reply.writer import HAIKU_VARIANTS, PROMPTS_DIR, Reply, write_reply  # noqa: E402
from tools.local_trial import _load_stock_problem  # noqa: E402
from tools.probe_metrics import aggregate  # noqa: E402


DATA_DIR = REPO_ROOT / "content/umigame-stock/umigame-soup-1/judge-trial/data"
# Haiku's dedicated templates must not invalidate the other providers' old caches.
PROMPT_VERSION = prompt_version(exclude_names=frozenset({"haiku_judge.txt", "haiku_reply_1b.txt"}))
PATTERNS = (
    {"id": "luna-1b", "label": "① luna + 1b", "judge_mode": "luna", "reply_variant": "1b"},
    {"id": "luna-1d", "label": "② luna + 1d-luna", "judge_mode": "luna", "reply_variant": "1d-luna"},
    {"id": "jev-2c", "label": "⑤ jev + 2c-luna", "judge_mode": "jev", "reply_variant": "2c-luna"},
    *({"id": f"haiku-1b-{effort}", "label": f"⑦ haiku + 1b-haiku（{effort}）",
       "judge_mode": "haiku", "reply_variant": "1b-haiku", "haiku_effort": effort}
      for effort in ("max", "xhigh", "high")),
    {"id": "luna-1b-haiku", "label": "⑨ luna + 1b-haiku", "judge_mode": "luna",
     "reply_variant": "1b-haiku", "haiku_effort": "high"},
    {"id": "jev-1b-haiku", "label": "⑩ jev + 1b-haiku", "judge_mode": "jev",
     "reply_variant": "1b-haiku", "haiku_effort": "high"},
)
PATTERN_IDS = tuple(item["id"] for item in PATTERNS)
LEGACY_PATTERN_IDS = ("luna-1b", "luna-1d", "jev-2c")
DEFAULT_PATTERN_IDS = ("haiku-1b-high", "luna-1b-haiku", "jev-1b-haiku")
JudgeIndex = tuple[str, str, str | None]


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_case(entry: Any, no: str, source: str) -> dict[str, Any]:
    if not isinstance(entry, dict) or not {"id", "text", "kind"} <= entry.keys():
        raise ValueError(f"{source} case requires id, text and kind: {entry!r}")
    kind = entry["kind"]
    if kind not in KINDS:
        raise ValueError(f"invalid kind for {entry['id']}: {kind}")
    answer = entry.get("answer")
    if kind == "q_yesno" and answer not in {"yes", "no", "irrelevant"}:
        raise ValueError(f"q_yesno case {entry['id']} needs yes/no/irrelevant answer")
    for accepted in entry.get("accept_kinds", []):
        if accepted not in KINDS:
            raise ValueError(f"invalid accept_kinds for {entry['id']}: {accepted}")
    for accepted in entry.get("accept_answers", []):
        if accepted not in ANSWERS:
            raise ValueError(f"invalid accept_answers for {entry['id']}: {accepted}")
    return {"id": str(entry["id"]), "no": no, "text": str(entry["text"]),
            "expected_kind": kind, "expected_answer": answer,
            "accept_kinds": list(entry.get("accept_kinds", [])),
            "accept_answers": list(entry.get("accept_answers", [])), "source": source}


def load_cases(only: list[str] | None = None, *,
               eval_path: Path | None = None, bare_term_path: Path | None = None,
               common_path: Path | None = None) -> list[dict[str, Any]]:
    """Load and validate cases, assigning common cases round-robin."""
    eval_data = _json(eval_path or DATA_DIR / "eval_problems.json")
    bare_path = bare_term_path or DATA_DIR / "bare_term_cases.json"
    bare_data = _json(bare_path) if bare_path.is_file() else {}
    common = _json(common_path or DATA_DIR / "common_cases.json")
    if not isinstance(eval_data, dict) or not eval_data:
        raise ValueError("eval_problems.json must be a nonempty object")
    if not isinstance(bare_data, dict) or not isinstance(common, list):
        raise ValueError("bare_term_cases.json must be an object and common_cases.json an array")
    selected = [no for no in eval_data if only is None or no in only]
    unknown = [no for no in (only or []) if no not in eval_data]
    if unknown:
        raise ValueError(f"unknown problems: {', '.join(unknown)}")
    if not selected:
        raise ValueError("no problems selected")
    cases = []
    for no in selected:
        if not isinstance(eval_data[no], list):
            raise ValueError(f"eval cases for {no} must be an array")
        cases.extend(_normalize_case(entry, no, "eval") for entry in eval_data[no])
        bare = bare_data.get(no, [])
        if not isinstance(bare, list):
            raise ValueError(f"bare term cases for {no} must be an array")
        cases.extend(_normalize_case(entry, no, "bare_term") for entry in bare)
    cases.extend(_normalize_case(entry, selected[i % len(selected)], "common")
                 for i, entry in enumerate(common))
    seen = set()
    for case in cases:
        if case["id"] in seen:
            raise ValueError(f"duplicate case id: {case['id']}")
        seen.add(case["id"])
    return cases


def _key(parts: Any) -> str:
    raw = json.dumps(parts, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _content_hash(case: dict[str, Any], problem: Problem) -> str:
    return _key([case["text"], problem.content_key,
                 list(problem.core_points), list(problem.fact_sheet),
                 {"points": list(problem.judge_criteria.points),
                  "errors": list(problem.judge_criteria.errors)}])


def _judge_cache_key(
    case: dict[str, Any], problem: Problem, method: str, model: str, *,
    haiku_effort: str = "high", luna_effort: str = "xhigh",
) -> str:
    """Isolate judges by effort and the inputs that affect their results."""
    cache_model = (anthropic_util.MODEL if method == "haiku" else
                   model if method == "luna" else None)
    parts = [case["id"], method, PROMPT_VERSION, _content_hash(case, problem), cache_model]
    if method == "luna":
        parts.append(luna_effort)
    elif method == "jev":
        parts.extend((jev.T_POINT, jev.T_CLOSE))
    elif method == "haiku":
        parts.extend((haiku_effort, hashlib.sha256(haiku.RULES_PATH.read_bytes()).hexdigest()))
    return _key(parts)


def _haiku_writer_effort(pattern: dict[str, Any]) -> str:
    return pattern.get("haiku_effort", "high") if pattern["reply_variant"] == "1b-haiku" else "low"


def _writer_cache_key(
    pattern: dict[str, Any], case: dict[str, Any], problem: Problem, combined: Any, model: str,
) -> str:
    """Isolate the truth writers by provider, effort and prompt."""
    cache_model = anthropic_util.MODEL if pattern["reply_variant"] in HAIKU_VARIANTS else model
    parts = [pattern["id"], case["id"], PROMPT_VERSION,
             [combined.kind, combined.answer, combined.bare_term, combined.decision],
             _content_hash(case, problem), cache_model]
    if pattern["reply_variant"] == "1b":
        parts.append(pattern.get("luna_effort", "xhigh"))
    elif pattern["reply_variant"] in HAIKU_VARIANTS:
        prompt_name = ("haiku_reply_1b.txt" if pattern["reply_variant"] == "1b-haiku"
                       else "reply_writer.txt")
        parts.extend((_haiku_writer_effort(pattern),
                      hashlib.sha256((PROMPTS_DIR / prompt_name).read_bytes()).hexdigest()))
    return _key(parts)


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                         encoding="utf-8")
    temporary.replace(path)


def _cache(path: Path) -> dict[str, Any]:
    return _json(path) if path.is_file() else {}


def _judge_entry(outcome: Judgement | Exception, elapsed: float) -> dict[str, Any]:
    if isinstance(outcome, Exception):
        failure = {"type": type(outcome).__name__, "message": str(outcome)}
        if hasattr(outcome, "debug"):
            failure["debug"] = outcome.debug
        return {"exception": failure,
                "elapsed_s": elapsed}
    return {"judgement": asdict(outcome), "elapsed_s": elapsed}


def _judge_outcome(entry: dict[str, Any]) -> Judgement | Exception:
    if "judgement" in entry:
        return Judgement(**entry["judgement"])
    error = entry["exception"]
    if error["type"] in {"AnthropicError", "AnthropicRefusalError"}:
        cls = getattr(anthropic_util, error["type"])
        return cls(error["message"], debug=error.get("debug", {}))
    cls = getattr(builtins, error["type"], RuntimeError)
    if not isinstance(cls, type) or not issubclass(cls, Exception):
        cls = RuntimeError
    outcome = cls(error["message"])
    if "debug" in error:
        outcome.debug = error["debug"]
    return outcome


def _timed_judge(method: str, call: Callable[..., Judgement], case: dict[str, Any],
                 problem: Problem, key: str, model: str, haiku_effort: str = "high",
                 luna_effort: str = "xhigh") -> dict[str, Any]:
    start = time.perf_counter()
    try:
        if method == "luna":
            outcome = call(case["id"], case["text"], problem, api_key=key, model=model,
                           effort=luna_effort)
        elif method == "haiku":
            outcome = call(case["id"], case["text"], problem, api_key=key, effort=haiku_effort)
        else:
            outcome = call(case["id"], case["text"], problem, api_key=key)
        if not isinstance(outcome, Judgement):
            raise TypeError(f"{method} returned {type(outcome).__name__}, expected Judgement")
    except Exception as exc:
        outcome = exc
    entry = _judge_entry(outcome, time.perf_counter() - start)
    if method == "haiku":
        logged = entry.get("judgement", entry.get("exception", {}))
        logged["debug"] = {**logged.get("debug", {}), "effort": haiku_effort}
    return entry


def _timed_writer(call: Callable[..., Reply], combined: Any, case: dict[str, Any],
                  problem: Problem, variant: str, key: str,
                  model: str, anthropic_key: str = "",
                  haiku_effort: str = "high", luna_effort: str = "xhigh") -> tuple[Reply | Exception, float]:
    start = time.perf_counter()
    try:
        reply = call(combined, case["id"], case["text"], problem,
                     variant=variant, openai_api_key=key, model=model,
                     luna_effort=luna_effort,
                     **({"anthropic_api_key": anthropic_key, "haiku_effort": haiku_effort}
                        if variant in HAIKU_VARIANTS else {}))
        if not isinstance(reply, Reply):
            raise TypeError(f"writer returned {type(reply).__name__}, expected Reply")
    except Exception as exc:
        reply = exc
    return reply, time.perf_counter() - start


def _judge_timing(entries: dict[str, dict[str, Any]]) -> dict[str, float | None]:
    """Sum only the sequential judge calls observed in this pattern."""
    judge_s = sum(entry["elapsed_s"] for entry in entries.values())
    return {**{f"{method}_s": entries.get(method, {}).get("elapsed_s")
               for method in ("luna", "jev", "haiku")},
            "judge_s": judge_s, "writer_s": None, "total_s": judge_s}


def _print_summary(metrics: dict[str, Any], patterns: list[dict[str, Any]]) -> None:
    names = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "L1_kind", "L1_kind_each",
             "L1_phrasing", "L1_guidance", "L2_one_liner", "L2_opener",
             "L2_conflict", "L2_proximity", "L2_emoji")
    print("pattern | " + " | ".join(names) + " | total median / p95 (s)")
    for pattern in patterns:
        data = metrics["patterns"][pattern["id"]]
        values = []
        for name in names:
            item = data["metrics"][name]
            mark = "○" if item["pass"] is True else "×" if item["pass"] is False else "—"
            values.append(f"{item['value']} {mark}")
        timing = data["reference"]["timing"]["total_s"]
        duration = (f"{timing['median']:.2f} / {timing['p95']:.2f}"
                    if timing["median"] is not None else "—")
        print(pattern["id"] + " | " + " | ".join(values) + " | " + duration)


def run_probe(*, out: Path, problems: list[str] | None = None,
              patterns: list[str] | None = None, workers: int = 4,
              refresh_judge: bool = False, refresh_writer: bool = False,
              eval_path: Path | None = None, bare_term_path: Path | None = None,
              common_path: Path | None = None,
              problem_loader: Callable[[str], Problem] = _load_stock_problem,
              luna_call: Callable[..., Judgement] = luna.judge,
              jev_call: Callable[..., Judgement] = jev.judge,
              haiku_call: Callable[..., Judgement] = haiku.judge,
              writer_call: Callable[..., Reply] = write_reply,
              api_keys: dict[str, str] | None = None,
              run_at: str | None = None) -> dict[str, Any]:
    """Run selected cases, sharing cached outcomes across each case's patterns.

    Python defaults to the remaining legacy patterns 1, 2 and 5. The CLI
    defaults to 7 (high), 9 and 10. Fallbacks run only after the main fails;
    independent cases and writers can run concurrently.
    """
    if workers < 1:
        raise ValueError("workers must be at least 1")
    base_config = Config.from_env()
    selected_ids = LEGACY_PATTERN_IDS if patterns is None else patterns
    selected_patterns = [
        {**p, "luna_effort": p.get("luna_effort", base_config.luna_effort),
         "haiku_effort": p.get("haiku_effort", base_config.haiku_effort)}
        for p in PATTERNS if p["id"] in selected_ids
    ]
    unknown_patterns = [p for p in selected_ids if p not in PATTERN_IDS]
    if unknown_patterns or not selected_patterns:
        raise ValueError(f"unknown or empty patterns: {', '.join(unknown_patterns)}")
    cases = load_cases(problems, eval_path=eval_path, bare_term_path=bare_term_path,
                       common_path=common_path)
    eval_data = _json(eval_path or DATA_DIR / "eval_problems.json")
    selected_nos = [no for no in eval_data if problems is None or no in problems]
    snapshots = {no: problem_loader(no) for no in selected_nos}
    model = base_config.luna_model
    keys = api_keys if api_keys is not None else {
        "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
        "typesafe_api_key": os.environ.get("TYPESAFE_API_KEY", ""),
        "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    }
    missing = []
    if ((any(p["judge_mode"] == "luna" for p in selected_patterns) and luna_call is luna.judge)
            or (any(p["reply_variant"] in {"1b", "1d-luna", "2c-luna"}
                    for p in selected_patterns) and writer_call is write_reply)):
        if not keys.get("openai_api_key"):
            missing.append("OPENAI_API_KEY")
    if any(p["judge_mode"] == "jev" for p in selected_patterns) and jev_call is jev.judge:
        if not keys.get("typesafe_api_key"):
            missing.append("TYPESAFE_API_KEY")
    if ((any(p["judge_mode"] == "haiku" for p in selected_patterns) and haiku_call is haiku.judge)
            or (any(p["reply_variant"] in HAIKU_VARIANTS for p in selected_patterns)
                and writer_call is write_reply)):
        if not keys.get("anthropic_api_key"):
            missing.append("ANTHROPIC_API_KEY")
    if missing:
        raise ValueError("missing API key environment variable(s): " + ", ".join(missing))

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    judge_path, writer_path = out / "judge_cache.json", out / "writer_cache.json"
    judge_cache, writer_cache = _cache(judge_path), _cache(writer_path)
    judge_entries: dict[JudgeIndex, dict[str, Any]] = {}
    judge_status: dict[JudgeIndex, str] = {}
    run_at = run_at or utc_now()
    counts = {no: {source: sum(case["no"] == no and case["source"] == source for case in cases)
                   for source in ("eval", "bare_term", "common")}
              for no in selected_nos}
    results: dict[str, Any] = {
        "meta": {"run_at": run_at, "prompt_version": PROMPT_VERSION,
                 "luna_model": model, "problems": selected_nos,
                 "patterns": selected_patterns, "case_counts": counts},
        "problems": {no: {"problem_text": problem.problem_text,
                           "content_key": problem.content_key,
                           "core_points": list(problem.core_points)}
                     for no, problem in snapshots.items()},
        "cases": cases, "rows": {p["id"]: [] for p in selected_patterns},
    }

    def judge_case(case: dict[str, Any]) -> tuple[dict, dict, dict, dict]:
        problem = snapshots[case["no"]]
        entries: dict[JudgeIndex, dict[str, Any]] = {}
        status: dict[JudgeIndex, str] = {}
        fresh: dict[str, dict[str, Any]] = {}
        rows = {}
        for pattern in selected_patterns:
            config = Config(
                judge_mode=pattern["judge_mode"], reply_variant=pattern["reply_variant"],
                haiku_effort=pattern["haiku_effort"], luna_effort=pattern["luna_effort"],
                luna_model=model, set_code=problem.set_code,
            )
            comment = {"id": case["id"], "text": case["text"],
                       "from": {"id": "probe"}, "media": {"id": problem.media_id}}
            record = new_record(comment, None, run_at, config, problem)
            observed: dict[str, dict[str, Any]] = {}
            cache = dict.fromkeys(("luna", "jev", "haiku", "writer"), "none")

            def cached_judge(method: str) -> Judgement:
                effort = {"luna": config.luna_effort, "haiku": config.haiku_effort}.get(method)
                index = case["id"], method, effort
                if index not in entries:
                    cache_key = _judge_cache_key(
                        case, problem, method, model,
                        haiku_effort=config.haiku_effort, luna_effort=config.luna_effort,
                    )
                    if not refresh_judge and cache_key in judge_cache:
                        entries[index], status[index] = judge_cache[cache_key], "hit"
                    else:
                        call = {"luna": luna_call, "jev": jev_call, "haiku": haiku_call}[method]
                        api_key_name = {"jev": "typesafe_api_key", "haiku": "anthropic_api_key"}.get(
                            method, "openai_api_key",
                        )
                        entries[index] = _timed_judge(
                            method, call, case, problem, keys.get(api_key_name, ""), model,
                            config.haiku_effort, config.luna_effort,
                        )
                        status[index] = "miss"
                        fresh[cache_key] = entries[index]
                observed[method] = entries[index]
                cache[method] = status[index]
                outcome = _judge_outcome(entries[index])
                if isinstance(outcome, Exception):
                    raise outcome
                return outcome

            combined: Combined | None = None
            try:
                combined = combine(
                    case["id"], case["text"], problem, config, keys,
                    luna_call=lambda *a, **k: cached_judge("luna"),
                    jev_call=lambda *a, **k: cached_judge("jev"),
                    haiku_call=lambda *a, **k: cached_judge("haiku"),
                )
            except Exception as exc:
                record["errors"].append(f"processing: {type(exc).__name__}: {exc}")
                for method, entry in observed.items():
                    outcome = _judge_outcome(entry)
                    logged = outcome if isinstance(outcome, Judgement) else Judgement(
                        method, None, error=str(outcome), debug=getattr(outcome, "debug", {}),
                    )
                    record["judgements"][method] = logged.as_log()
            row = {"case_id": case["id"], "no": case["no"], "record": record,
                   "timing": _judge_timing(observed), "cache": cache}
            rows[pattern["id"]] = row, combined
        return rows, entries, status, fresh

    case_rows = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(judge_case, case): case["id"] for case in cases}
        for completed, future in enumerate(as_completed(futures), 1):
            rows, entries, status, fresh = future.result()
            case_rows[futures[future]] = rows
            judge_entries.update(entries)
            judge_status.update(status)
            judge_cache.update(fresh)
            if fresh and completed % 5 == 0:
                _atomic_json(judge_path, judge_cache)
    if any(value == "miss" for value in judge_status.values()):
        _atomic_json(judge_path, judge_cache)

    writer_futures = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for pattern in selected_patterns:
            for case in cases:
                row, combined = case_rows[case["id"]][pattern["id"]]
                results["rows"][pattern["id"]].append(row)
                if combined is None:
                    continue
                problem = snapshots[case["no"]]
                writer_key = _writer_cache_key(pattern, case, problem, combined, model)
                if not refresh_writer and writer_key in writer_cache:
                    cached = writer_cache[writer_key]
                    reply = Reply(**cached["reply"])
                    row["timing"]["writer_s"] = cached["elapsed_s"]
                    row["timing"]["total_s"] += cached["elapsed_s"]
                    row["cache"]["writer"] = "hit"
                    apply_decision(row["record"], combined, reply, judged_at=run_at)
                else:
                    future = pool.submit(
                        _timed_writer, writer_call, combined, case, problem,
                        pattern["reply_variant"], keys.get("openai_api_key", ""), model,
                        keys.get("anthropic_api_key", ""), pattern["haiku_effort"],
                        pattern["luna_effort"],
                    )
                    writer_futures[future] = (row, combined, writer_key)
        completed = 0
        for future in as_completed(writer_futures):
            row, combined, writer_key = writer_futures[future]
            reply, elapsed = future.result()
            row["timing"]["writer_s"] = elapsed
            row["timing"]["total_s"] += elapsed
            row["cache"]["writer"] = "miss"
            if isinstance(reply, Exception):
                apply_decision(row["record"], combined,
                               Reply(None, "no_reply", False, debug=getattr(reply, "debug", {})),
                               judged_at=run_at)
                row["record"]["errors"].append(f"processing: {type(reply).__name__}: {reply}")
            else:
                writer_cache[writer_key] = {"reply": asdict(reply), "elapsed_s": elapsed}
                apply_decision(row["record"], combined, reply, judged_at=run_at)
                completed += 1
                if completed % 5 == 0:
                    _atomic_json(writer_path, writer_cache)
    if writer_futures:
        _atomic_json(writer_path, writer_cache)
    efforts = dict.fromkeys((*(index[2] for index in judge_entries if index[1] == "haiku"), *(
        _haiku_writer_effort(p) for p in selected_patterns if p["reply_variant"] in HAIKU_VARIANTS
    )))
    for effort in efforts:
        totals = _anthropic_totals(results, judge_entries, judge_status, effort=effort)
        fresh = _anthropic_totals(results, judge_entries, judge_status,
                                  effort=effort, fresh_only=True)
        fields = (*anthropic_util.USAGE_FIELDS, "refusals")
        print(f"Anthropic ({effort}): " + ", ".join(f"{key}={totals[key]}" for key in fields)
              + " (new: " + ", ".join(f"{key}={fresh[key]}" for key in fields) + ")")
    metrics = aggregate(results)
    _atomic_json(out / "results.json", results)
    _atomic_json(out / "metrics.json", metrics)
    _print_summary(metrics, selected_patterns)
    return results


def _anthropic_totals(
    results: dict[str, Any], entries: dict[JudgeIndex, dict[str, Any]],
    status: dict[JudgeIndex, str], *, effort: str, fresh_only: bool = False,
) -> dict[str, int]:
    """Sum one effort's shared judge calls and writer calls without double counting."""
    debug_items = [entry.get("judgement", entry.get("exception", {})).get("debug", {})
                   for index, entry in entries.items() if index[1:] == ("haiku", effort)
                   and (not fresh_only or status[index] == "miss")]
    debug_items.extend((row["record"].get("reply") or {}).get("debug", {})
                       for pattern in results["meta"]["patterns"]
                       if pattern["reply_variant"] in HAIKU_VARIANTS
                       and _haiku_writer_effort(pattern) == effort
                       for row in results["rows"][pattern["id"]]
                       if not fresh_only or row["cache"]["writer"] == "miss")
    totals = {key: sum((debug.get("usage") or debug).get(key, 0) or 0 for debug in debug_items)
              for key in anthropic_util.USAGE_FIELDS}
    totals["refusals"] = sum(debug.get("stop_reason") == "refusal" for debug in debug_items)
    return totals


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problems", nargs="+", help="problem numbers; default: all eval problems")
    parser.add_argument("--patterns", nargs="+", choices=PATTERN_IDS,
                        help="pattern ids; default: " + " ".join(DEFAULT_PATTERN_IDS))
    parser.add_argument("--out", type=Path,
                        default=SERVICE_DIR / "work/probe" / utc_now().replace(":", "-"))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--refresh-judge", action="store_true")
    parser.add_argument("--refresh-writer", action="store_true")
    args = parser.parse_args(argv)
    try:
        run_probe(out=args.out, problems=args.problems,
                  patterns=args.patterns if args.patterns is not None else list(DEFAULT_PATTERN_IDS),
                  workers=args.workers, refresh_judge=args.refresh_judge,
                  refresh_writer=args.refresh_writer)
    except (ValueError, FileNotFoundError) as exc:
        parser.exit(2, f"probe_run: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
