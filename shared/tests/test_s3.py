"""Tests for S3 object storage helpers."""

from unittest.mock import Mock

from acps_shared import generate_presigned_url, get_object, put_object


def test_get_object_reads_injected_client_body() -> None:
    """The helper downloads and reads the complete response body."""
    client = Mock()
    client.get_object.return_value = {"Body": Mock(read=Mock(return_value=b"audio"))}

    assert get_object("bucket", "audio/track.m4a", client=client) == b"audio"
    client.get_object.assert_called_once_with(
        Bucket="bucket",
        Key="audio/track.m4a",
    )


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
