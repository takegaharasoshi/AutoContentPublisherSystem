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

from app.comment_log import PROMPT_VERSION, apply_decision, new_record, utc_now  # noqa: E402
from app.config import Config  # noqa: E402
from app.judge import decisions, jev, luna  # noqa: E402
from app.judge.combiner import combine  # noqa: E402
from app.judge.contract import ANSWERS, Judgement, KINDS, Problem  # noqa: E402
from app.reply.writer import Reply, write_reply  # noqa: E402
from tools.local_trial import _load_stock_problem  # noqa: E402
from tools.probe_metrics import aggregate  # noqa: E402


DATA_DIR = REPO_ROOT / "content/umigame-stock/umigame-soup-1/judge-trial/data"
PATTERNS = (
    {"id": "luna-1b", "label": "① luna + 1b", "judge_mode": "luna", "shadow": False,
     "consensus": False, "reply_variant": "1b"},
    {"id": "luna-1d", "label": "② luna + 1d-luna", "judge_mode": "luna", "shadow": False,
     "consensus": False, "reply_variant": "1d-luna"},
    {"id": "hybrid-1d", "label": "③ hybrid + 1d-luna", "judge_mode": "hybrid", "shadow": True,
     "consensus": True, "reply_variant": "1d-luna"},
    {"id": "jev-2b", "label": "④ jev + 2b", "judge_mode": "jev", "shadow": False,
     "consensus": False, "reply_variant": "2b"},
    {"id": "jev-2c", "label": "⑤ jev + 2c-luna", "judge_mode": "jev", "shadow": False,
     "consensus": False, "reply_variant": "2c-luna"},
    {"id": "dec-2c", "label": "⑥ decisions + 2c-luna", "judge_mode": "decisions", "shadow": False,
     "consensus": False, "reply_variant": "2c-luna"},
)
PATTERN_IDS = tuple(item["id"] for item in PATTERNS)
LEGACY_PATTERN_IDS = PATTERN_IDS[:-1]


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
        if isinstance(outcome, decisions.DecisionsError):
            failure["debug"] = outcome.debug
        return {"exception": failure,
                "elapsed_s": elapsed}
    return {"judgement": asdict(outcome), "elapsed_s": elapsed}


def _judge_outcome(entry: dict[str, Any]) -> Judgement | Exception:
    if "judgement" in entry:
        return Judgement(**entry["judgement"])
    error = entry["exception"]
    if error["type"] == "DecisionsError":
        return decisions.DecisionsError(error["message"], debug=error.get("debug", {}))
    cls = getattr(builtins, error["type"], RuntimeError)
    if not isinstance(cls, type) or not issubclass(cls, Exception):
        cls = RuntimeError
    return cls(error["message"])


def _timed_judge(method: str, call: Callable[..., Judgement], case: dict[str, Any],
                 problem: Problem, key: str, model: str) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        if method in {"luna", "decisions"}:
            outcome = call(case["id"], case["text"], problem, api_key=key, model=model)
        else:
            outcome = call(case["id"], case["text"], problem, api_key=key)
        if not isinstance(outcome, Judgement):
            raise TypeError(f"{method} returned {type(outcome).__name__}, expected Judgement")
    except Exception as exc:
        outcome = exc
    return _judge_entry(outcome, time.perf_counter() - start)


def _timed_writer(call: Callable[..., Reply], combined: Any, case: dict[str, Any],
                  problem: Problem, variant: str, key: str,
                  model: str) -> tuple[Reply | Exception, float]:
    start = time.perf_counter()
    try:
        reply = call(combined, case["id"], case["text"], problem,
                     variant=variant, openai_api_key=key, model=model)
        if not isinstance(reply, Reply):
            raise TypeError(f"writer returned {type(reply).__name__}, expected Reply")
    except Exception as exc:
        reply = exc
    return reply, time.perf_counter() - start


def _judge_timing(pattern: dict[str, Any], entries: dict[str, dict[str, Any]],
                  decision: str | None) -> dict[str, float | None]:
    mode = pattern["judge_mode"]
    if mode == "decisions":
        decisions_s = entries["decisions"]["elapsed_s"]
        luna_s = (entries["luna"]["elapsed_s"]
                  if decision == "decisions_fallback_luna" else None)
        judge_s = decisions_s + (luna_s or 0)
        return {"luna_s": luna_s, "jev_s": None, "decisions_s": decisions_s,
                "judge_s": judge_s, "writer_s": None, "total_s": judge_s}
    luna_s = (entries["luna"]["elapsed_s"]
              if mode != "jev" or decision == "jev_fallback_luna" else None)
    jev_s = entries["jev"]["elapsed_s"] if mode != "luna" else None
    if mode == "hybrid":
        judge_s = max(luna_s or 0, jev_s or 0)
    elif mode == "jev":
        judge_s = (jev_s or 0) + (luna_s or 0)
    else:
        judge_s = luna_s or 0
    return {"luna_s": luna_s, "jev_s": jev_s, "judge_s": judge_s,
            "writer_s": None, "total_s": judge_s}


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
              decisions_call: Callable[..., Judgement] = decisions.judge,
              writer_call: Callable[..., Reply] = write_reply,
              api_keys: dict[str, str] | None = None,
              run_at: str | None = None) -> dict[str, Any]:
    """Run selected cases; the Python default preserves the legacy five patterns.

    The CLI explicitly selects all six when --patterns is omitted.
    Injected calls support fully offline tests.
    """
    if workers < 1:
        raise ValueError("workers must be at least 1")
    selected_ids = LEGACY_PATTERN_IDS if patterns is None else patterns
    selected_patterns = [p for p in PATTERNS if p["id"] in selected_ids]
    unknown_patterns = [p for p in (patterns or []) if p not in PATTERN_IDS]
    if unknown_patterns or not selected_patterns:
        raise ValueError(f"unknown or empty patterns: {', '.join(unknown_patterns)}")
    cases = load_cases(problems, eval_path=eval_path, bare_term_path=bare_term_path,
                       common_path=common_path)
    selected_nos = list(dict.fromkeys(case["no"] for case in cases))
    # A selected problem can have zero cases; preserve its metadata and assignment order.
    eval_data = _json(eval_path or DATA_DIR / "eval_problems.json")
    selected_nos = [no for no in eval_data if problems is None or no in problems]
    snapshots = {no: problem_loader(no) for no in selected_nos}
    model = os.environ.get("LUNA_MODEL", "gpt-6-luna")
    keys = api_keys if api_keys is not None else {
        "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
        "typesafe_api_key": os.environ.get("TYPESAFE_API_KEY", ""),
    }
    need_jev = any(p["judge_mode"] in {"jev", "hybrid"} for p in selected_patterns)
    need_decisions = any(p["judge_mode"] == "decisions" for p in selected_patterns)
    methods = ("luna",) + (("jev",) if need_jev else ()) + (
        ("decisions",) if need_decisions else ()
    )
    missing = []
    if (luna_call is luna.judge or writer_call is write_reply or
            (need_decisions and decisions_call is decisions.judge)) and not keys.get("openai_api_key"):
        missing.append("OPENAI_API_KEY")
    if need_jev and jev_call is jev.judge and not keys.get("typesafe_api_key"):
        missing.append("TYPESAFE_API_KEY")
    if missing:
        raise ValueError("missing API key environment variable(s): " + ", ".join(missing))

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    judge_path, writer_path = out / "judge_cache.json", out / "writer_cache.json"
    judge_cache, writer_cache = _cache(judge_path), _cache(writer_path)
    judge_entries: dict[tuple[str, str], dict[str, Any]] = {}
    judge_status: dict[tuple[str, str], str] = {}
    futures = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for case in cases:
            problem = snapshots[case["no"]]
            for method in methods:
                cache_key = _key([
                    case["id"], method, PROMPT_VERSION, _content_hash(case, problem),
                    model if method in {"luna", "decisions"} else None,
                ])
                index = case["id"], method
                if not refresh_judge and cache_key in judge_cache:
                    judge_entries[index] = judge_cache[cache_key]
                    judge_status[index] = "hit"
                else:
                    call = {"luna": luna_call, "jev": jev_call, "decisions": decisions_call}[method]
                    api_key_name = "typesafe_api_key" if method == "jev" else "openai_api_key"
                    api_key = keys.get(api_key_name, "")
                    future = pool.submit(_timed_judge, method, call, case, problem, api_key, model)
                    futures[future] = (index, cache_key)
        completed = 0
        for future in as_completed(futures):
            index, cache_key = futures[future]
            entry = future.result()
            judge_cache[cache_key] = entry
            judge_entries[index] = entry
            judge_status[index] = "miss"
            completed += 1
            if completed % 5 == 0:
                _atomic_json(judge_path, judge_cache)
    if futures:
        _atomic_json(judge_path, judge_cache)
    if need_decisions:
        totals = {"input_tokens": 0, "calls": 0}
        fresh = {"input_tokens": 0, "calls": 0}
        for index, entry in judge_entries.items():
            if index[1] != "decisions":
                continue
            debug = entry.get("judgement", entry.get("exception", {})).get("debug", {})
            for key in totals:
                totals[key] += debug.get(key, 0)
                if judge_status[index] == "miss":
                    fresh[key] += debug.get(key, 0)
        print(f"Decisions: input_tokens={totals['input_tokens']}, calls={totals['calls']} "
              f"(new: input_tokens={fresh['input_tokens']}, calls={fresh['calls']})")

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
        "cases": cases, "rows": {},
    }
    writer_futures = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for pattern in selected_patterns:
            config_by_no = {
                no: Config(
                    judge_mode=pattern["judge_mode"], shadow=pattern["shadow"],
                    consensus=pattern["consensus"], reply_variant=pattern["reply_variant"],
                    luna_model=model, set_code=snapshots[no].set_code,
                ) for no in selected_nos
            }
            rows = []
            results["rows"][pattern["id"]] = rows
            for case in cases:
                case_id, no = case["id"], case["no"]
                problem = snapshots[no]
                config = config_by_no[no]
                comment = {"id": case_id, "text": case["text"],
                           "from": {"id": "probe"}, "media": {"id": problem.media_id}}
                record = new_record(comment, None, run_at, config, problem)
                supplied = {method: _judge_outcome(judge_entries[case_id, method])
                            for method in methods}
                relevant = {method: judge_entries[case_id, method]
                            for method in methods}
                cache = {method: judge_status.get((case_id, method), "none")
                         if (method == "luna" or need_jev) else "none"
                         for method in ("luna", "jev")}
                if pattern["judge_mode"] == "decisions":
                    cache["decisions"] = judge_status[case_id, "decisions"]
                    cache["jev"] = "none"
                cache["writer"] = "none"
                try:
                    combined = combine(case_id, case["text"], problem, config, keys,
                                       precomputed=supplied)
                except Exception as exc:
                    record["errors"].append(f"processing: {type(exc).__name__}: {exc}")
                    mode = pattern["judge_mode"]
                    staged_failed = mode in {"jev", "decisions"} and (
                        isinstance(supplied.get(mode), Exception) or
                        bool(getattr(supplied.get(mode), "error", None))
                    )
                    fallback_decision = (
                        f"{mode}_fallback_luna" if staged_failed else None
                    )
                    timing = _judge_timing(pattern, relevant, fallback_decision)
                    if mode in {"jev", "decisions"} and not staged_failed:
                        cache["luna"] = "none"
                    if pattern["judge_mode"] == "luna":
                        cache["jev"] = "none"
                    rows.append({"case_id": case_id, "no": no, "record": record,
                                 "timing": timing, "cache": cache})
                    continue
                timing = _judge_timing(pattern, relevant, combined.decision)
                if pattern["judge_mode"] in {"jev", "decisions"} and not combined.decision.endswith(
                    "_fallback_luna"
                ):
                    cache["luna"] = "none"
                if pattern["judge_mode"] == "luna":
                    cache["jev"] = "none"
                row = {"case_id": case_id, "no": no, "record": record,
                       "timing": timing, "cache": cache}
                rows.append(row)
                writer_key = _key([pattern["id"], case_id, PROMPT_VERSION,
                                   [combined.kind, combined.answer, combined.bare_term,
                                    combined.decision], _content_hash(case, problem), model])
                if not refresh_writer and writer_key in writer_cache:
                    cached = writer_cache[writer_key]
                    reply = Reply(**cached["reply"])
                    timing["writer_s"] = cached["elapsed_s"]
                    timing["total_s"] += cached["elapsed_s"]
                    cache["writer"] = "hit"
                    apply_decision(record, combined, reply, judged_at=run_at)
                else:
                    future = pool.submit(
                        _timed_writer, writer_call, combined, case, problem,
                        pattern["reply_variant"], keys.get("openai_api_key", ""), model,
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
                row["record"]["errors"].append(f"processing: {type(reply).__name__}: {reply}")
            else:
                writer_cache[writer_key] = {"reply": asdict(reply), "elapsed_s": elapsed}
                apply_decision(row["record"], combined, reply, judged_at=run_at)
                completed += 1
                if completed % 5 == 0:
                    _atomic_json(writer_path, writer_cache)
    if writer_futures:
        _atomic_json(writer_path, writer_cache)
    metrics = aggregate(results)
    _atomic_json(out / "results.json", results)
    _atomic_json(out / "metrics.json", metrics)
    _print_summary(metrics, selected_patterns)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problems", nargs="+", help="problem numbers; default: all eval problems")
    parser.add_argument("--patterns", nargs="+", choices=PATTERN_IDS,
                        help="pattern ids; default: all")
    parser.add_argument("--out", type=Path,
                        default=SERVICE_DIR / "work/probe" / utc_now().replace(":", "-"))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--refresh-judge", action="store_true")
    parser.add_argument("--refresh-writer", action="store_true")
    args = parser.parse_args(argv)
    try:
        run_probe(out=args.out, problems=args.problems,
                  patterns=args.patterns if args.patterns is not None else list(PATTERN_IDS),
                  workers=args.workers, refresh_judge=args.refresh_judge,
                  refresh_writer=args.refresh_writer)
    except (ValueError, FileNotFoundError) as exc:
        parser.exit(2, f"probe_run: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
