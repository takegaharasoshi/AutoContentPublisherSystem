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


SET_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SET_DIR.parents[2]
SERVICE_DIR = REPO_ROOT / "services/comment-reply"
for _path in (SERVICE_DIR, SET_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from app.comment_log import apply_decision, new_record, utc_now, write_record  # noqa: E402
from app.config import Config, HAIKU_EFFORTS, LUNA_EFFORTS, REPLY_VARIANTS  # noqa: E402
from app.judge import haiku, jev, luna  # noqa: E402
from app.judge.combiner import combine  # noqa: E402
from app.judge.contract import Judgement, Problem  # noqa: E402
from app.reply.writer import HAIKU_VARIANTS, write_reply  # noqa: E402


STOCK_PATH = REPO_ROOT / "content/umigame-stock/umigame-soup-1/batch-01/stock_items.py"
# Same numbered combinations as probe_run.PATTERNS.
PATTERNS = {
    "1": ("luna", "1b"), "2": ("luna", "1d-luna"),
    "5": ("jev", "2c-luna"), "7": ("haiku", "1b-haiku"),
    "9": ("luna", "1b-haiku"), "10": ("jev", "1b-haiku"),
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
                        choices=("luna", "jev", "haiku"),
                        default=["luna", "jev", "haiku"])
    parser.add_argument("--patterns", nargs="+", choices=sorted(PATTERNS, key=int),
                        help="evaluation patterns (mode + reply variant), e.g. 7 9 10; "
                             "overrides --modes and --reply-variant")
    parser.add_argument("--haiku-effort", nargs="+", choices=sorted(HAIKU_EFFORTS),
                        help="effort(s) for the Haiku judge and 1b-haiku writer; several values "
                             "run each Haiku pattern once per effort (default: HAIKU_EFFORT)")
    parser.add_argument("--luna-effort", nargs="+", choices=sorted(LUNA_EFFORTS),
                        help="effort(s) for the Luna judge and 1b writer (default: LUNA_EFFORT)")
    parser.add_argument("--reply-variant", choices=sorted(REPLY_VARIANTS))
    parser.add_argument("--stub-judgements", type=Path, help="offline judge fixture JSON")
    parser.add_argument("--out", type=Path, default=SERVICE_DIR / "work/local_trial")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run selected modes, sharing outcomes and calling fallbacks only as needed."""
    args = _parser().parse_args(argv)
    problem = _load_stock_problem(args.problem) if args.problem else Problem.from_snapshot(
        json.loads(args.snapshot.read_text(encoding="utf-8"))
    )
    base_config = Config.from_env()
    haiku_efforts = list(dict.fromkeys(args.haiku_effort or [base_config.haiku_effort]))
    luna_efforts = list(dict.fromkeys(args.luna_effort or [base_config.luna_effort]))
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

    # (output label, judge mode, reply variant)
    if args.patterns:
        runs = [(f"p{no}-{PATTERNS[no][0]}-{PATTERNS[no][1]}", *PATTERNS[no])
                for no in args.patterns]
        if stub_rows:
            runs = [(label, mode, "2b") for label, mode, _ in runs]
    else:
        runs = [(mode, mode, variant) for mode in args.modes]
    expanded = []
    for label, mode, run_variant in runs:
        uses_haiku = mode == "haiku" or run_variant in HAIKU_VARIANTS
        uses_luna = mode == "luna" or run_variant == "1b"
        for haiku_effort in haiku_efforts if uses_haiku else haiku_efforts[:1]:
            for luna_effort in luna_efforts if uses_luna else luna_efforts[:1]:
                suffix = f"-{haiku_effort}" if uses_haiku and len(haiku_efforts) > 1 else ""
                if uses_luna and len(luna_efforts) > 1:
                    suffix += f"-luna-{luna_effort}"
                expanded.append((label + suffix, mode, run_variant, haiku_effort, luna_effort))
    runs = expanded
    modes = {run[1] for run in runs}
    keys = {"openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
            "typesafe_api_key": os.environ.get("TYPESAFE_API_KEY", ""),
            "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", "")}
    if not stub_rows:
        missing = []
        if ("luna" in modes or any(run[2] in {"1b", "1d-luna", "2c-luna"}
                                   for run in runs)) and not keys["openai_api_key"]:
            missing.append("OPENAI_API_KEY")
        if "jev" in modes and not keys["typesafe_api_key"]:
            missing.append("TYPESAFE_API_KEY")
        needs_anthropic = "haiku" in modes or any(run[2] in HAIKU_VARIANTS for run in runs)
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
        outcomes: dict[tuple[str, str | None], Judgement | Exception] = {}
        print(f"\n{comment_text}")
        for label, mode, run_variant, haiku_effort, luna_effort in runs:
            config = Config(
                judge_mode=mode, reply_variant=run_variant, luna_model=base_config.luna_model,
                haiku_effort=haiku_effort, luna_effort=luna_effort, set_code=problem.set_code,
            )
            seconds: dict[str, float] = {}

            def cached_judge(method: str, **kwargs: Any) -> Judgement:
                effort = kwargs.get("effort")
                cache_key = method, effort
                name = f"{method}({effort})" if effort else method
                if cache_key not in outcomes:
                    started = time.monotonic()
                    try:
                        if fixture:
                            if method not in fixture:
                                raise ValueError(f"stub entry lacks {method}: {comment_text}")
                            outcomes[cache_key] = _stub_result(method, fixture[method])
                        else:
                            call = {"luna": luna.judge, "jev": jev.judge, "haiku": haiku.judge}[method]
                            outcomes[cache_key] = call(comment_id, comment_text, problem, **kwargs)
                    except Exception as exc:
                        outcomes[cache_key] = exc
                    seconds[name] = time.monotonic() - started
                outcome = outcomes[cache_key]
                if isinstance(outcome, Exception):
                    raise outcome
                return outcome

            combined = combine(
                comment_id, comment_text, problem, config, keys,
                luna_call=lambda *a, **k: cached_judge("luna", **k),
                jev_call=lambda *a, **k: cached_judge("jev", **k),
                haiku_call=lambda *a, **k: cached_judge("haiku", **k),
            )
            judged_at = utc_now()
            if seconds:
                print("  判定の所要: " + " / ".join(f"{k} {v:.1f}秒" for k, v in seconds.items()))
            started = time.monotonic()
            reply = write_reply(
                combined, comment_id, comment_text, problem, variant=run_variant,
                openai_api_key=keys["openai_api_key"], model=config.luna_model,
                anthropic_api_key=keys["anthropic_api_key"], haiku_effort=config.haiku_effort,
                luna_effort=config.luna_effort,
            )
            writer_seconds = time.monotonic() - started
            comment = {"id": comment_id, "text": comment_text,
                       "from": {"id": "local-user"}, "media": {"id": problem.media_id}}
            record = new_record(comment, None, received_at, config, problem)
            apply_decision(record, combined, reply, judged_at=judged_at)
            path = write_record(record, directory=args.out / label)
            files.append(path)
            print(f"  {label}: {combined.kind} / {combined.answer or '-'} / {combined.decision}"
                  f" | {reply.text or '(返信なし)'}"
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
