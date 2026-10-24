"""Read and write the two S3 state documents without storing comment bodies."""

from __future__ import annotations

import json
from typing import Any


def read_json(bucket: str, key: str, *, client: Any = None) -> dict | None:
    """Read an object; only NoSuchKey/404 means absence, never AccessDenied."""
    if client is None:
        import boto3

        client = boto3.client("s3")
    try:
        response = client.get_object(Bucket=bucket, Key=key)
    except Exception as exc:
        response = getattr(exc, "response", {})
        code = response.get("Error", {}).get("Code")
        if str(code) in {"NoSuchKey", "404", "NotFound"}:
            return None
        raise
    body = response["Body"]
    try:
        data = json.loads(body.read().decode("utf-8"))
    finally:
        body.close()
    if not isinstance(data, dict):
        raise ValueError("S3 document must contain a JSON object")
    return data


def write_json(bucket: str, key: str, data: dict, *, client: Any = None) -> None:
    """Persist UTF-8 JSON, propagating failures to the caller."""
    if client is None:
        import boto3

        client = boto3.client("s3")
    client.put_object(
        Bucket=bucket, Key=key, ContentType="application/json",
        Body=json.dumps(data, ensure_ascii=False).encode("utf-8"),
    )


def get_media_counts(bucket: str, prefix: str, *, client: Any = None) -> dict:
    """Return previous comment counts, or an empty document on first use."""
    data = read_json(bucket, f"{prefix}media-counts.json", client=client)
    if data is None:
        return {"media": {}}
    if not isinstance(data.get("media"), dict):
        raise ValueError("media-counts.media must be an object")
    for entry in data["media"].values():
        if not isinstance(entry, dict) or type(entry.get("comments_count")) is not int:
            raise ValueError("invalid media comment count")
    return data


def put_media_counts(bucket: str, prefix: str, data: dict, *, client: Any = None) -> None:
    """Save completed media counts."""
    write_json(bucket, f"{prefix}media-counts.json", data, client=client)


def get_judged(bucket: str, prefix: str, media_id: str, *, client: Any = None) -> dict:
    """Return terminal judgments and pending failure counters for a post."""
    data = read_json(bucket, f"{prefix}judged/{media_id}.json", client=client)
    if data is None:
        return {"media_id": media_id, "first_correct_replied": False, "comments": {}}
    if (data.get("media_id") != media_id
            or type(data.get("first_correct_replied")) is not bool
            or not isinstance(data.get("comments"), dict)
            or any(not isinstance(value, dict) for value in data["comments"].values())):
        raise ValueError("invalid judged state")
    return data


def put_judged(
    bucket: str, prefix: str, media_id: str, data: dict, *, client: Any = None,
) -> None:
    """Save the post state after every successful reply and at post completion."""
    write_json(bucket, f"{prefix}judged/{media_id}.json", data, client=client)
