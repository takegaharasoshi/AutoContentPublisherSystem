"""Tests for prompt processing behavior."""

import datetime
from unittest.mock import Mock

import app.processing as processing
from app.models import PromptConfig


def _prompt(prompt_id: int) -> PromptConfig:
    """Build a simple prompt configuration."""
    return PromptConfig(prompt_id, 1, f"prompt {prompt_id}", None, None)


def _run(
    monkeypatch,
    prompt_configs: list[PromptConfig],
    generator,
    has_image,
) -> tuple[processing.ProcessingResult, Mock, Mock]:
    """Run processing with injectable image existence behavior."""
    cursor = Mock()
    connection = Mock()
    monkeypatch.setattr(processing, "has_generated_image", has_image)
    monkeypatch.setattr(processing, "put_object", Mock())
    monkeypatch.setattr(processing, "insert_generated_image", Mock(return_value=1))
    result = processing.process_prompt_configs(
        cursor,
        connection,
        set_id=1,
        set_code="set-a",
        scheduled_at=datetime.datetime(2026, 7, 19),
        generation_run_id=2,
        prompt_configs=prompt_configs,
        generator=generator,
        s3_bucket="bucket",
        s3_client=Mock(),
    )
    return result, connection, processing.put_object


def test_processing_skips_existing_prompt_and_counts_only_new_images(monkeypatch) -> None:
    """Already completed prompts are neither generated nor uploaded."""
    calls: list[int] = []

    def generator(prompt_config: PromptConfig) -> list[bytes]:
        calls.append(prompt_config.id)
        return [b"new"]

    def has_image(cursor, run_id, prompt_id) -> bool:
        del cursor, run_id
        call_counts[prompt_id] = call_counts.get(prompt_id, 0) + 1
        return prompt_id == 1 or call_counts[prompt_id] > 1

    call_counts: dict[int, int] = {}
    result, connection, put_object = _run(
        monkeypatch, [_prompt(1), _prompt(2)], generator, has_image
    )

    assert result == processing.ProcessingResult(1, True)
    assert calls == [2]
    assert put_object.call_count == 1
    connection.commit.assert_called_once()


def test_processing_continues_after_generator_error_and_empty_result(monkeypatch) -> None:
    """Per-prompt generator failures do not stop following prompt configs."""
    def generator(prompt_config: PromptConfig) -> list[bytes]:
        if prompt_config.id == 1:
            raise RuntimeError("secret-like detail")
        if prompt_config.id == 2:
            return []
        return [b"ok"]

    call_counts: dict[int, int] = {}

    def has_image(cursor, run_id, prompt_id) -> bool:
        del cursor, run_id
        call_counts[prompt_id] = call_counts.get(prompt_id, 0) + 1
        return prompt_id == 3 and call_counts[prompt_id] > 1

    result, _, put_object = _run(
        monkeypatch,
        [_prompt(1), _prompt(2), _prompt(3)],
        generator,
        has_image,
    )

    assert result == processing.ProcessingResult(1, False)
    put_object.assert_called_once()


def test_processing_allows_s3_orphan_and_continues_other_outputs(monkeypatch) -> None:
    """A DB failure after upload leaves an allowed orphan and processing continues."""
    cursor = Mock()
    connection = Mock()
    uploaded: list[str] = []
    inserted_ids: list[int] = []
    first_insert = True

    monkeypatch.setattr(processing, "has_generated_image", lambda *args: False)

    def upload(bucket, key, body, **kwargs) -> None:
        del bucket, body, kwargs
        uploaded.append(key)

    def insert(cursor_arg, **kwargs) -> int:
        nonlocal first_insert
        del cursor_arg
        inserted_ids.append(kwargs["output_index"])
        if first_insert:
            first_insert = False
            raise RuntimeError("db failure")
        return 1

    monkeypatch.setattr(processing, "put_object", upload)
    monkeypatch.setattr(processing, "insert_generated_image", insert)

    result = processing.process_prompt_configs(
        cursor,
        connection,
        set_id=1,
        set_code="set-a",
        scheduled_at=datetime.datetime(2026, 7, 19),
        generation_run_id=2,
        prompt_configs=[_prompt(1), _prompt(2)],
        generator=lambda prompt_config: (
            [b"first", b"second"]
            if prompt_config.id == 1
            else [b"third"]
        ),
        s3_bucket="bucket",
        s3_client=Mock(),
    )

    assert uploaded == [
        "images/set-a/20260719/2/1_0.jpg",
        "images/set-a/20260719/2/1_1.jpg",
        "images/set-a/20260719/2/2_0.jpg",
    ]
    assert inserted_ids == [0, 1, 0]
    assert result == processing.ProcessingResult(2, False)
    assert connection.commit.call_count == 2


def test_processing_uses_final_database_recheck_for_completion(monkeypatch) -> None:
    """A skipped prompt is complete when the final DB recheck confirms it."""
    calls: list[int] = []

    def has_image(cursor, run_id, prompt_id) -> bool:
        del cursor, run_id
        calls.append(prompt_id)
        return prompt_id == 1 or calls.count(prompt_id) > 1

    result, _, _ = _run(
        monkeypatch,
        [_prompt(1), _prompt(2)],
        lambda prompt_config: [b"image"],
        has_image,
    )

    assert result.all_prompt_configs_complete
    assert calls == [1, 2, 1, 2]
