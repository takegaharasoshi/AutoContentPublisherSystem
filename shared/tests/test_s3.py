"""Tests for S3 object storage helpers."""

from unittest.mock import Mock

from acps_shared import put_object


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
