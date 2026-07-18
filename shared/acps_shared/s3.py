"""S3 object storage helpers."""

from __future__ import annotations

from typing import Any

import boto3


def put_object(
    bucket: str,
    key: str,
    body: bytes,
    *,
    content_type: str = "application/octet-stream",
    client: Any | None = None,
) -> None:
    """Upload an object to S3.

    Args:
        bucket: Destination S3 bucket name.
        key: Destination object key.
        body: Object content.
        content_type: MIME type for the object.
        client: Optional S3 client, for dependency injection.
    """
    s3_client = client if client is not None else boto3.client("s3")
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType=content_type,
    )
