"""Tests for final-media processing behavior."""

import datetime
from unittest.mock import Mock

import app.processing as processing
from app.generators import (
    GeneratorResult,
    IntermediateOutput,
    MediaOutput,
)
from app.models import PromptConfig


def _prompt(prompt_id: int) -> PromptConfig:
    """Build a simple prompt configuration."""
    return PromptConfig(prompt_id, 1, f"prompt {prompt_id}", None, None)


def _process(
    monkeypatch,
    *,
    generator,
    prompt_configs: list[PromptConfig] | None = None,
    has_media=None,
    put_object=None,
    insert_media=None,
) -> tuple[processing.ProcessingResult, Mock, Mock, Mock]:
    """Run processing with injectable persistence behavior."""
    cursor = Mock()
    connection = Mock()
    has_media = has_media or (lambda *args: False)
    put_object = put_object or Mock()
    insert_media = insert_media or Mock(return_value=1)
    monkeypatch.setattr(processing, "has_generated_media", has_media)
    monkeypatch.setattr(processing, "put_object", put_object)
    monkeypatch.setattr(processing, "insert_generated_media", insert_media)
    result = processing.process_prompt_configs(
        cursor,
        connection,
        set_id=1,
        set_code="set-a",
        scheduled_at=datetime.datetime(2026, 7, 19),
        generation_run_id=2,
        prompt_configs=prompt_configs or [_prompt(1)],
        generator=generator,
        s3_bucket="bucket",
        s3_client=Mock(),
    )
    return result, connection, put_object, insert_media


def test_processing_skips_existing_prompt_and_counts_new_media(monkeypatch) -> None:
    """Completed prompts are neither generated nor uploaded."""
    generated_ids: list[int] = []
    calls: dict[int, int] = {}

    def has_media(cursor, run_id, prompt_id) -> bool:
        del cursor, run_id
        calls[prompt_id] = calls.get(prompt_id, 0) + 1
        return prompt_id == 1 or calls[prompt_id] > 1

    def generator(context):
        generated_ids.append(context.prompt_config.id)
        return GeneratorResult([MediaOutput(b"new", "jpg")])

    result, connection, put_object, _ = _process(
        monkeypatch,
        generator=generator,
        prompt_configs=[_prompt(1), _prompt(2)],
        has_media=has_media,
    )

    assert result == processing.ProcessingResult(1, True)
    assert generated_ids == [2]
    put_object.assert_called_once()
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()


def test_processing_passes_schedule_and_run_id_to_generator(monkeypatch) -> None:
    """Normalized execution identity is supplied through GeneratorContext."""
    observed = {}

    def generator(context):
        observed["scheduled_at"] = context.scheduled_at
        observed["generation_run_id"] = context.generation_run_id
        return GeneratorResult([MediaOutput(b"image", "jpg")])

    _process(monkeypatch, generator=generator)

    assert observed == {
        "scheduled_at": datetime.datetime(2026, 7, 19),
        "generation_run_id": 2,
    }


def test_processing_passes_final_media_metadata_to_insert(monkeypatch) -> None:
    """All final-media metadata is persisted and controls S3 storage."""
    media = MediaOutput(
        b"video",
        "mp4",
        width=1080,
        height=1920,
        duration_seconds=10,
        audio_asset_id=7,
    )
    result, connection, put_object, insert_media = _process(
        monkeypatch,
        generator=lambda context: GeneratorResult([media]),
    )

    assert result.new_media_inserted == 1
    put_object.assert_called_once()
    assert put_object.call_args.args[:3] == (
        "bucket",
        "videos/set-a/20260719/2/1_0.mp4",
        b"video",
    )
    assert put_object.call_args.kwargs["content_type"] == "video/mp4"
    inserted = insert_media.call_args.kwargs
    assert inserted["file_format"] == "mp4"
    assert inserted["width"] == 1080
    assert inserted["height"] == 1920
    assert inserted["duration_seconds"] == 10
    assert inserted["audio_asset_id"] == 7
    connection.commit.assert_called_once()


def test_processing_stores_intermediate_without_database_insert(monkeypatch) -> None:
    """A source JPEG is uploaded under videos but never inserted."""
    generated = GeneratorResult(
        [MediaOutput(b"video", "mp4", 1080, 1920, 10, 4)],
        [IntermediateOutput(b"source", "jpg", "_source", 0)],
    )
    _, _, put_object, insert_media = _process(
        monkeypatch,
        generator=lambda context: generated,
    )

    assert [call.args[1] for call in put_object.call_args_list] == [
        "videos/set-a/20260719/2/1_0_source.jpg",
        "videos/set-a/20260719/2/1_0.mp4",
    ]
    assert [call.kwargs["content_type"] for call in put_object.call_args_list] == [
        "image/jpeg",
        "video/mp4",
    ]
    insert_media.assert_called_once()


def test_processing_resolves_png_intermediate_content_type(monkeypatch) -> None:
    """PNG intermediates use image/png while sharing the video prefix."""
    generated = GeneratorResult(
        [MediaOutput(b"video", "mp4")],
        [IntermediateOutput(b"cut", "png", "_cut1", 0)],
    )
    _, _, put_object, _ = _process(
        monkeypatch,
        generator=lambda context: generated,
    )

    intermediate_call = put_object.call_args_list[0]
    assert intermediate_call.args[1].endswith("_cut1.png")
    assert intermediate_call.kwargs["content_type"] == "image/png"


def test_intermediate_upload_failure_does_not_stop_final_media(monkeypatch) -> None:
    """Debug artifact failures do not affect final upload or registration."""
    put_object = Mock(side_effect=[RuntimeError("source failed"), None])
    generated = GeneratorResult(
        [MediaOutput(b"video", "mp4")],
        [IntermediateOutput(b"source", "jpg", "_source", 0)],
    )

    result, connection, _, insert_media = _process(
        monkeypatch,
        generator=lambda context: generated,
        put_object=put_object,
    )

    assert result.new_media_inserted == 1
    assert put_object.call_count == 2
    insert_media.assert_called_once()
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()


def test_generator_failure_rolls_back_and_continues(monkeypatch) -> None:
    """Generator-side auxiliary updates are rolled back on failure."""
    def generator(context):
        if context.prompt_config.id == 1:
            raise RuntimeError("generation failed")
        return GeneratorResult([MediaOutput(b"ok", "jpg")])

    result, connection, _, _ = _process(
        monkeypatch,
        generator=generator,
        prompt_configs=[_prompt(1), _prompt(2)],
    )

    assert result.new_media_inserted == 1
    assert connection.rollback.call_count == 1
    assert connection.commit.call_count == 1


def test_insert_failure_rolls_back_and_continues_outputs(monkeypatch) -> None:
    """An INSERT failure rolls back before a later output is attempted."""
    insert_media = Mock(side_effect=[RuntimeError("db failed"), 2])
    generated = GeneratorResult(
        [MediaOutput(b"one", "jpg"), MediaOutput(b"two", "jpg")]
    )

    result, connection, put_object, _ = _process(
        monkeypatch,
        generator=lambda context: generated,
        insert_media=insert_media,
    )

    assert result.new_media_inserted == 1
    assert put_object.call_count == 2
    connection.rollback.assert_called_once()
    connection.commit.assert_called_once()


def test_final_media_upload_failure_rolls_back(monkeypatch) -> None:
    """An S3 failure rolls back generator-side auxiliary table updates."""
    put_object = Mock(side_effect=RuntimeError("s3 failed"))

    result, connection, _, insert_media = _process(
        monkeypatch,
        generator=lambda context: GeneratorResult(
            [MediaOutput(b"video", "mp4")]
        ),
        put_object=put_object,
    )

    assert result.new_media_inserted == 0
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    insert_media.assert_not_called()


def test_empty_result_rolls_back_and_is_incomplete(monkeypatch) -> None:
    """An empty result cannot leave generator-side DB changes pending."""
    result, connection, put_object, _ = _process(
        monkeypatch,
        generator=lambda context: GeneratorResult([]),
    )

    assert result == processing.ProcessingResult(0, False)
    connection.rollback.assert_called_once()
    put_object.assert_not_called()
