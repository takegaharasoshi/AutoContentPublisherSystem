"""Run production judges and writer locally, without importing boto3."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parents[1]
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from app.comment_log import apply_decision, new_record, utc_now, write_record  # noqa: E402
from app.config import Config, HAIKU_EFFORTS, REPLY_VARIANTS  # noqa: E402
from app.judge import decisions, haiku, jev, luna  # noqa: E402
from app.judge.combiner import combine  # noqa: E402
from app.judge.contract import Judgement, Problem  # noqa: E402
from app.reply.writer import HAIKU_VARIANTS, write_reply  # noqa: E402


STOCK_PATH = REPO_ROOT / "content/umigame-stock/umigame-soup-1/batch-01/stock_items.py"
# Same combinations as probe_run.PATTERNS (21-6e compares 1, 2, 5 and 7 by hand).
PATTERNS = {
    "1": ("luna", "1b", False, False), "2": ("luna", "1d-luna", False, False),
    "3": ("hybrid", "1d-luna", True, True), "4": ("jev", "2b", False, False),
    "5": ("jev", "2c-luna", False, False), "6": ("decisions", "2c-luna", False, False),
    "7": ("haiku", "1b-haiku", False, False), "8": ("haiku", "1d-haiku", False, False),
}


def _load_stock_problem(no: str) -> Problem:
    """Make a production-shaped snapshot from ITEMS and JUDGE_POINTS."""
    spec = importlib.util.spec_from_file_location("local_umigame_stock_items", STOCK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STOCK_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    item = next((row for row in module.ITEMS if row.get("no") == no), None)
    if item is None:
        raise ValueError(f"problem {no} was not found in {STOCK_PATH}")
    points = module.JUDGE_POINTS.get(no)
    if not isinstance(points, dict):
        raise ValueError(f"JUDGE_POINTS has no entry for {no}")
    return Problem.from_snapshot({
        "schema_version": 3, "set_code": "umigame-soup-1",
        "media_id": f"local-{no}", "content_key": item["content_key"],
        "problem_text": item["problem_text"], "truth": item["truth"],
        "fact_sheet": item["fact_sheet"], "core_points": points["core_points"],
        "judge_criteria": points["judge_criteria"],
        "reveal_text": points["reveal_text"],
    })


def _stub_result(method: str, raw: dict[str, Any]) -> Judgement | Exception:
    """Turn a compact fixture into an actual judge outcome."""
    if raw.get("error"):
        return RuntimeError(str(raw["error"]))
    return Judgement(
        method, raw["kind"], answer=raw.get("answer"),
        reason=raw.get("reason", "local stub"), bare_term=raw.get("bare_term"),
        debug={"model": "stub"},
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--problem", help="ID from batch-01/stock_items.py, e.g. U01")
    source.add_argument("--snapshot", type=Path, help="published schema-v3 snapshot JSON")
    parser.add_argument("--comment", action="append", default=[], help="comment; repeatable")
    parser.add_argument("--comments-file", type=Path, help="one comment per line")
    parser.add_argument("--modes", nargs="+",
                        choices=("luna", "jev", "hybrid", "decisions", "haiku"),
                        default=["luna", "jev", "hybrid"])
    parser.add_argument("--patterns", nargs="+", choices=sorted(PATTERNS),
                        help="evaluation patterns (mode + reply variant), e.g. 1 2 5 7; "
                             "overrides --modes and --reply-variant")
    parser.add_argument("--haiku-effort", nargs="+", choices=sorted(HAIKU_EFFORTS),
                        help="effort(s) for the Haiku judge and 1b-haiku writer; several values "
                             "run each Haiku pattern once per effort (default: HAIKU_EFFORT)")
    parser.add_argument("--reply-variant", choices=sorted(REPLY_VARIANTS))
    parser.add_argument("--shadow", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--consensus", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--stub-judgements", type=Path, help="offline judge fixture JSON")
    parser.add_argument("--out", type=Path, default=SERVICE_DIR / "work/local_trial")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run each judge once per comment, then replay outcomes through each mode."""
    args = _parser().parse_args(argv)
    problem = _load_stock_problem(args.problem) if args.problem else Problem.from_snapshot(
        json.loads(args.snapshot.read_text(encoding="utf-8"))
    )
    base_config = Config.from_env()
    haiku_efforts = list(dict.fromkeys(args.haiku_effort or [base_config.haiku_effort]))
    variant = args.reply_variant or base_config.reply_variant
    stub_rows: list[dict[str, Any]] = []
    if args.stub_judgements:
        loaded = json.loads(args.stub_judgements.read_text(encoding="utf-8"))
        stub_rows = loaded["comments"] if isinstance(loaded, dict) else loaded
        if not isinstance(stub_rows, list):
            raise ValueError("stub file must contain a comments array")
        if variant != "2b" or args.patterns:
            print("stub mode: LLM writer variant uses 2b templates")
            variant = "2b"
    comments = list(args.comment)
    if args.comments_file:
        comments.extend(line for line in args.comments_file.read_text(encoding="utf-8").splitlines() if line)
    if not comments and stub_rows:
        comments = [str(row["comment"]) for row in stub_rows]
    if not comments:
        print("コメントを1行ずつ入力してください。空行で終了します。")
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            if not line:
                break
            comments.append(line)

    effective_shadow = base_config.shadow if args.shadow is None else args.shadow
    effective_consensus = base_config.consensus if args.consensus is None else args.consensus
    # (output label, judge mode, reply variant, shadow, consensus)
    if args.patterns:
        runs = [(f"p{no}-{PATTERNS[no][0]}-{PATTERNS[no][1]}", *PATTERNS[no])
                for no in args.patterns]
        if stub_rows:
            runs = [(label, mode, "2b", shadow, consensus)
                    for label, mode, _, shadow, consensus in runs]
    else:
        runs = [(mode, mode, variant, effective_shadow, effective_consensus)
                for mode in args.modes]
    # Haiku patterns run once per effort; the others carry an unused effort.
    expanded = []
    for label, mode, run_variant, shadow, consensus in runs:
        uses_haiku = mode == "haiku" or run_variant in HAIKU_VARIANTS
        for effort in haiku_efforts if uses_haiku else haiku_efforts[:1]:
            suffix = f"-{effort}" if uses_haiku and len(haiku_efforts) > 1 else ""
            expanded.append((label + suffix, mode, run_variant, shadow, consensus, effort))
    runs = expanded
    modes = {run[1] for run in runs}
    needs_luna = bool(modes & {"luna", "hybrid", "jev", "decisions"})
    needs_decisions = "decisions" in modes
    needs_haiku = "haiku" in modes
    needs_jev = "jev" in modes or any(
        mode == "hybrid" and (shadow or consensus) for _, mode, _, shadow, consensus, _ in runs
    )
    keys = {"openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
            "typesafe_api_key": os.environ.get("TYPESAFE_API_KEY", ""),
            "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", "")}
    if not stub_rows:
        missing = []
        if needs_luna and not keys["openai_api_key"]:
            missing.append("OPENAI_API_KEY")
        if needs_jev and not keys["typesafe_api_key"]:
            missing.append("TYPESAFE_API_KEY")
        needs_anthropic = needs_haiku or any(run[2] in HAIKU_VARIANTS for run in runs)
        if needs_anthropic and not keys["anthropic_api_key"]:
            missing.append("ANTHROPIC_API_KEY")
        if missing:
            raise ValueError(f"missing API key environment variable(s): {', '.join(missing)}")

    files: list[str] = []
    # Run stamp keeps records of repeated runs on the same problem from overwriting each other.
    run_stamp = time.strftime("%H%M%S")
    for index, comment_text in enumerate(comments, 1):
        fixture = next((row for row in stub_rows if row.get("comment") == comment_text), None)
        if stub_rows and fixture is None:
            raise ValueError(f"stub has no judgement for comment: {comment_text}")
        comment_id = str(fixture.get("id") if fixture else f"{problem.media_id}-{run_stamp}-{index}")
        received_at = utc_now()
        outcomes: dict[str, Judgement | Exception] = {}
        haiku_outcomes: dict[str, Judgement | Exception] = {}
        seconds: dict[str, float] = {}
        if fixture:
            methods = ("luna", "jev") + (("decisions",) if needs_decisions else ()) + (
                ("haiku",) if needs_haiku else ())
            for method in methods:
                if method not in fixture:
                    raise ValueError(f"stub entry lacks {method}: {comment_text}")
                outcomes[method] = _stub_result(method, fixture[method])
            if needs_haiku:
                haiku_outcomes = {effort: outcomes["haiku"] for effort in haiku_efforts}
        else:
            if needs_luna:
                started = time.monotonic()
                try:
                    outcomes["luna"] = luna.judge(
                        comment_id, comment_text, problem,
                        api_key=keys["openai_api_key"], model=base_config.luna_model,
                    )
                except Exception as exc:
                    outcomes["luna"] = exc
                seconds["luna"] = time.monotonic() - started
            if needs_jev:
                started = time.monotonic()
                try:
                    outcomes["jev"] = jev.judge(
                        comment_id, comment_text, problem, api_key=keys["typesafe_api_key"],
                    )
                except Exception as exc:
                    outcomes["jev"] = exc
                seconds["jev"] = time.monotonic() - started
            if needs_decisions:
                started = time.monotonic()
                try:
                    outcomes["decisions"] = decisions.judge(
                        comment_id, comment_text, problem,
                        api_key=keys["openai_api_key"], model=base_config.luna_model,
                    )
                except Exception as exc:
                    outcomes["decisions"] = exc
                seconds["decisions"] = time.monotonic() - started
            for effort in haiku_efforts if needs_haiku else ():
                started = time.monotonic()
                try:
                    haiku_outcomes[effort] = haiku.judge(
                        comment_id, comment_text, problem,
                        api_key=keys["anthropic_api_key"], effort=effort,
                    )
                except Exception as exc:
                    haiku_outcomes[effort] = exc
                seconds[f"haiku({effort})"] = time.monotonic() - started
        judged_at = utc_now()
        print(f"\n{comment_text}")
        if seconds:
            print("  判定の所要: " + " / ".join(f"{k} {v:.1f}秒" for k, v in seconds.items()))
        for label, mode, run_variant, shadow, consensus, haiku_effort in runs:
            config = Config(
                judge_mode=mode, shadow=shadow, consensus=consensus,
                reply_variant=run_variant, luna_model=base_config.luna_model,
                haiku_effort=haiku_effort,
                set_code=problem.set_code,
            )
            combined = combine(
                comment_id, comment_text, problem, config, keys,
                precomputed={**outcomes, **(
                    {"haiku": haiku_outcomes[haiku_effort]} if haiku_effort in haiku_outcomes
                    else {})},
            )
            started = time.monotonic()
            reply = write_reply(
                combined, comment_id, comment_text, problem, variant=run_variant,
                openai_api_key=keys["openai_api_key"], model=config.luna_model,
                anthropic_api_key=keys["anthropic_api_key"], haiku_effort=config.haiku_effort,
            )
            writer_seconds = time.monotonic() - started
            comment = {"id": comment_id, "text": comment_text,
                       "from": {"id": "local-user"}, "media": {"id": problem.media_id}}
            record = new_record(comment, None, received_at, config, problem)
            apply_decision(record, combined, reply, judged_at=judged_at)
            path = write_record(record, directory=args.out / label)
            files.append(path)
            print(f"  {label}: {combined.kind} / {combined.answer or '-'} / {combined.decision}"
                  f" | {reply.text or '(返信なし)'} | mismatch={combined.mismatch}"
                  f" | 返信 {writer_seconds:.1f}秒")
    print("\n記録ファイル:")
    for path in files:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as exc:
        raise SystemExit(f"local_trial: {exc}") from exc
