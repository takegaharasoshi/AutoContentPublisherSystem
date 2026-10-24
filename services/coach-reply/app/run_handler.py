"""Scheduled quiz reply orchestration with incremental S3 checkpoints."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from app import first_correct, graph_api, judge, reply_text, secrets, selection
from app import snapshot_store, state_store, switch
from app.config import Config


LOGGER = logging.getLogger(__name__)
logging.getLogger("app").setLevel(logging.INFO)
MIN_REMAINING_MS = 30_000
MAX_FAILURES = 3


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _low_time(context: Any) -> bool:
    return context is not None and context.get_remaining_time_in_millis() < MIN_REMAINING_MS


def _record(verdict: str, switch_value: str, **fields: Any) -> dict:
    return {
        "verdict": verdict, "confidence": None, "reason": "", "replied": False,
        "reply_id": None, "first": False, "switch": switch_value, "judged_at": _now(),
        "fail_count": 0, **fields,
    }


def _process_media(
    media: dict, snapshot: dict, config: Config, controls: switch.ReplySwitch,
    credentials: dict, own_username: str, context: Any, summary: dict,
) -> bool:
    """Return True only when the post's previous count can safely advance."""
    media_id = media["id"]
    state = state_store.get_judged(config.assets_bucket, config.state_prefix, media_id)
    comments = graph_api.list_comments(media_id, credentials["ig_access_token"],
                                       base_url=config.graph_api_base)
    selected = selection.select_comments(comments, own_username, state["comments"], controls.not_before)
    records = state["comments"]
    for verdict, excluded in (("operator_replied", selected.operator_replied),
                               ("before_start", selected.before_start)):
        for comment in excluded:
            records[comment["id"]] = _record(verdict, controls.value)

    state_store.put_judged(config.assets_bucket, config.state_prefix, media_id, state)
    candidates = sorted(
        selected.candidates,
        key=lambda comment: switch.parse_utc_timestamp(comment["timestamp"]),
    )
    pending_failure = False
    deferred = False
    # Finish each chronological batch before judging the next one. Completed
    # replies and silent judgments must survive even when a busy post is deferred.
    for offset in range(0, len(candidates), judge.MAX_BATCH_SIZE):
        if _low_time(context):
            deferred = True
            break
        batch = candidates[offset:offset + judge.MAX_BATCH_SIZE]
        timeout = 60.0
        if context is not None:
            available = context.get_remaining_time_in_millis() / 1000 - 10
            timeout = min(timeout, max(1.0, available))
        results = judge.judge_comments(
            snapshot, [{"id": c["id"], "text": c["text"]} for c in batch],
            config=config, api_key=credentials["anthropic_api_key"], timeout=timeout,
        )
        summary["judged"] += len(results)
        for comment in batch:
            cid = comment["id"]
            if cid in results:
                continue
            summary["judge_failures"] += 1
            fail_count = records.get(cid, {}).get("fail_count", 0) + 1
            if fail_count >= MAX_FAILURES:
                records[cid] = _record(
                    "judge_failed", controls.value, fail_count=fail_count,
                )
            else:
                # Absence of a verdict means this is still waiting for judgment.
                records[cid] = {
                    "fail_count": fail_count, "judged_at": _now(),
                    "switch": controls.value, "replied": False,
                }
                pending_failure = True

        # Older batches are already saved. All results in this batch are needed
        # to prove that every earlier answer was wrong, regardless of API order.
        chronology = {**records, **results}
        state_store.put_judged(
            config.assets_bucket, config.state_prefix, media_id, state,
        )
        for comment in batch:
            cid = comment["id"]
            result = results.get(cid)
            if result is None:
                continue
            record = _record(
                result["verdict"], controls.value,
                confidence=result["confidence"], reason=result["reason"],
            )
            if (result["verdict"] == "correct"
                    and result["confidence"] == "high"):
                first = first_correct.is_first_correct(
                    comment, selected.top_level, chronology,
                    first_correct_replied=state["first_correct_replied"],
                    has_operator_reply=selected.has_operator_reply,
                )
                record["first"] = first
                if controls.enabled:
                    if _low_time(context):
                        deferred = True
                        continue
                    message = reply_text.make_reply(
                        comment.get("username"), first=first,
                    )
                    record["reply_id"] = graph_api.post_reply(
                        cid, message, credentials["ig_access_token"],
                        base_url=config.graph_api_base,
                    )
                    record["replied"] = True
                    summary["replied"] += 1
                    if first:
                        state["first_correct_replied"] = True
            records[cid] = record
            if record["replied"]:
                state_store.put_judged(
                    config.assets_bucket, config.state_prefix, media_id, state,
                )
        state_store.put_judged(
            config.assets_bucket, config.state_prefix, media_id, state,
        )
        if deferred:
            break
    if deferred:
        summary["deferred"] += 1
    return not pending_failure and not deferred


def lambda_handler(event: Any, context: Any) -> dict:
    """Run chapter 1 steps 1–10, returning the same counters as the INFO summary.

    Invalid controls and infrastructure/Graph errors propagate so Lambda alarms
    can report them. Completed post counts are still saved in the final checkpoint.
    """
    summary = {
        "media": 0, "selected": 0, "read": 0, "no_snapshot": 0,
        "judged": 0, "replied": 0, "judge_failures": 0, "failures": 0, "deferred": 0,
    }
    counts = None
    config = Config.from_env()
    try:
        config.require("secret_arn", "assets_bucket", "param_prefix")
        controls = switch.read_switch(config.param_prefix)
        credentials = secrets.get_secrets(config.secret_arn)
        secrets.require_keys(credentials, "ig_access_token", "anthropic_api_key")
        own_username = graph_api.me(credentials["ig_access_token"],
                                     base_url=config.graph_api_base)["username"]
        media_list = graph_api.list_media(credentials["ig_access_token"], base_url=config.graph_api_base)
        summary["media"] = len(media_list)
        counts = state_store.get_media_counts(config.assets_bucket, config.state_prefix)
        changed = [media for media in media_list
                   if counts["media"].get(media["id"], {}).get("comments_count") != media["comments_count"]]
        summary["selected"] = len(changed)
        for index, media in enumerate(changed):
            if _low_time(context):
                summary["deferred"] += len(changed) - index
                break
            media_id = media["id"]
            snapshot = snapshot_store.get_snapshot(config.assets_bucket, config.problems_prefix, media_id)
            if snapshot is None:
                summary["no_snapshot"] += 1
                completed = True
            else:
                summary["read"] += 1
                completed = _process_media(media, snapshot, config, controls, credentials,
                                           own_username, context, summary)
            if completed:
                counts["media"][media_id] = {"comments_count": media["comments_count"], "checked_at": _now()}
    except Exception:
        summary["failures"] += 1
        raise
    finally:
        try:
            if counts is not None:
                counts["updated_at"] = _now()
                state_store.put_media_counts(config.assets_bucket, config.state_prefix, counts)
        except Exception:
            summary["failures"] += 1
            raise
        finally:
            LOGGER.info("coach_reply_summary %s", json.dumps(summary, separators=(",", ":")))
    return summary
