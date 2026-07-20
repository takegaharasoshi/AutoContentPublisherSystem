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


def generate_presigned_url(
    bucket: str,
    key: str,
    *,
    expires_in: int,
    client: Any | None = None,
) -> str:
    """Generate a presigned GET URL for an S3 object.

    Args:
        bucket: S3 bucket name.
        key: S3 object key.
        expires_in: URL validity duration in seconds.
        client: Optional S3 client, for dependency injection.

    Returns:
        A presigned HTTPS URL for downloading the object.
    """
    s3_client = client if client is not None else boto3.client("s3")
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
