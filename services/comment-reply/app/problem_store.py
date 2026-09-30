"""Published problem snapshot lookup."""

from __future__ import annotations

import json
from typing import Any

from app.judge.contract import Problem


class ProblemNotFound(LookupError):
    """No snapshot exists yet for the Instagram media ID."""


def get_problem(bucket: str, prefix: str, media_id: str, *, client: Any = None) -> Problem:
    """Read one S3 snapshot; only 404/NoSuchKey means absent."""
    if not media_id:
        raise ProblemNotFound("media_id is empty")
    if client is None:
        import boto3

        client = boto3.client("s3")
    try:
        result = client.get_object(Bucket=bucket, Key=f"{prefix}{media_id}.json")
    except Exception as exc:
        response = getattr(exc, "response", {})
        error = response.get("Error", {}) if isinstance(response, dict) else {}
        code = error.get("Code")
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode") if isinstance(response, dict) else None
        if str(code) in {"404", "NoSuchKey", "NotFound"} or status == 404:
            raise ProblemNotFound(media_id) from exc
        raise
    raw = json.loads(result["Body"].read().decode("utf-8"))
    problem = Problem.from_snapshot(raw)
    if problem.media_id != media_id:
        raise ValueError("snapshot media_id does not match requested media_id")
    return problem
