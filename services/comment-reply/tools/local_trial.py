"""Run production judges and writer locally, without importing boto3."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any


SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parents[1]
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from app.comment_log import apply_decision, new_record, utc_now, write_record  # noqa: E402
from app.config import Config, REPLY_VARIANTS  # noqa: E402
from app.judge import jev, luna  # noqa: E402
from app.judge.combiner import combine  # noqa: E402
from app.judge.contract import Judgement, Problem  # noqa: E402
from app.reply.writer import write_reply  # noqa: E402


STOCK_PATH = REPO_ROOT / "content/umigame-stock/umigame-soup-1/batch-01/stock_items.py"


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
    parser.add_argument("--modes", nargs="+", choices=("luna", "jev", "hybrid"),
                        default=["luna", "jev", "hybrid"])
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
    variant = args.reply_variant or base_config.reply_variant
    stub_rows: list[dict[str, Any]] = []
    if args.stub_judgements:
        loaded = json.loads(args.stub_judgements.read_text(encoding="utf-8"))
        stub_rows = loaded["comments"] if isinstance(loaded, dict) else loaded
        if not isinstance(stub_rows, list):
            raise ValueError("stub file must contain a comments array")
        if variant != "2b":
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

    needs_luna = "luna" in args.modes or "hybrid" in args.modes or "jev" in args.modes
    effective_shadow = base_config.shadow if args.shadow is None else args.shadow
    effective_consensus = base_config.consensus if args.consensus is None else args.consensus
    needs_jev = "jev" in args.modes or (
        "hybrid" in args.modes and (effective_shadow or effective_consensus)
    )
    keys = {"openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
            "typesafe_api_key": os.environ.get("TYPESAFE_API_KEY", "")}
    if not stub_rows:
        missing = []
        if needs_luna and not keys["openai_api_key"]:
            missing.append("OPENAI_API_KEY")
        if needs_jev and not keys["typesafe_api_key"]:
            missing.append("TYPESAFE_API_KEY")
        if missing:
            raise ValueError(f"missing API key environment variable(s): {', '.join(missing)}")

    files: list[str] = []
    for index, comment_text in enumerate(comments, 1):
        fixture = next((row for row in stub_rows if row.get("comment") == comment_text), None)
        if stub_rows and fixture is None:
            raise ValueError(f"stub has no judgement for comment: {comment_text}")
        comment_id = str(fixture.get("id") if fixture else f"{problem.media_id}-{index}")
        received_at = utc_now()
        outcomes: dict[str, Judgement | Exception] = {}
        if fixture:
            for method in ("luna", "jev"):
                if method not in fixture:
                    raise ValueError(f"stub entry lacks {method}: {comment_text}")
                outcomes[method] = _stub_result(method, fixture[method])
        else:
            if needs_luna:
                try:
                    outcomes["luna"] = luna.judge(
                        comment_id, comment_text, problem,
                        api_key=keys["openai_api_key"], model=base_config.luna_model,
                    )
                except Exception as exc:
                    outcomes["luna"] = exc
            if needs_jev:
                try:
                    outcomes["jev"] = jev.judge(
                        comment_id, comment_text, problem, api_key=keys["typesafe_api_key"],
                    )
                except Exception as exc:
                    outcomes["jev"] = exc
        judged_at = utc_now()
        print(f"\n{comment_text}")
        for mode in args.modes:
            config = Config(
                judge_mode=mode,
                shadow=base_config.shadow if args.shadow is None else args.shadow,
                consensus=base_config.consensus if args.consensus is None else args.consensus,
                reply_variant=variant, luna_model=base_config.luna_model,
                set_code=problem.set_code,
            )
            combined = combine(
                comment_id, comment_text, problem, config, keys,
                precomputed=outcomes,
            )
            reply = write_reply(
                combined, comment_id, comment_text, problem, variant=variant,
                openai_api_key=keys["openai_api_key"], model=config.luna_model,
            )
            comment = {"id": comment_id, "text": comment_text,
                       "from": {"id": "local-user"}, "media": {"id": problem.media_id}}
            record = new_record(comment, None, received_at, config, problem)
            apply_decision(record, combined, reply, judged_at=judged_at)
            path = write_record(record, directory=args.out / mode)
            files.append(path)
            print(f"  {mode}: {combined.kind} / {combined.answer or '-'} / {combined.decision}"
                  f" | {reply.text or '(返信なし)'} | mismatch={combined.mismatch}")
    print("\n記録ファイル:")
    for path in files:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as exc:
        raise SystemExit(f"local_trial: {exc}") from exc
