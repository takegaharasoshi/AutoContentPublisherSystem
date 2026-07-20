"""Tests for S3 object storage helpers."""

from unittest.mock import Mock

from acps_shared import generate_presigned_url, put_object


def test_put_object_uses_injected_client() -> None:
    """The helper forwards all object fields to the S3 client."""
    client = Mock()

    put_object(
        "example-bucket",
        "images/test.jpg",
        b"image-data",
        content_type="image/jpeg",
        client=client,
    )

    client.put_object.assert_called_once_with(
        Bucket="example-bucket",
        Key="images/test.jpg",
        Body=b"image-data",
        ContentType="image/jpeg",
    )


def test_generate_presigned_url_uses_injected_client() -> None:
    """The helper forwards bucket, key, and expiry to the S3 client."""
    client = Mock()
    client.generate_presigned_url.return_value = "https://example.com/signed"

    url = generate_presigned_url(
        "example-bucket",
        "images/test.jpg",
        expires_in=3600,
        client=client,
    )

    assert url == "https://example.com/signed"
    client.generate_presigned_url.assert_called_once_with(
        "get_object",
        Params={"Bucket": "example-bucket", "Key": "images/test.jpg"},
        ExpiresIn=3600,
    )
