"""Image batch application orchestration and logging setup."""

from __future__ import annotations

from typing import Any
import logging
import sys

import boto3

from acps_shared.db import open_connection
from acps_shared.secrets import get_db_secret, parse_db_secret

from .batch_sets import find_batch_set_by_code
from .clock import now_utc
from .config import ConfigError, load_config
from .execution_log import finalize_execution_log, start_or_resume_execution_log
from .generation_runs import parse_scheduled_at, resolve_generation_run
from .generators import resolve_generator
from .processing import process_prompt_configs
from .prompt_configs import fetch_active_prompt_configs


logger = logging.getLogger(__name__)


class BatchConfigError(Exception):
    """Raised when a selected batch set has no active prompt configurations."""


def setup_logging() -> None:
    """Configure stdout logging for the ECS awslogs log driver."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )


def main(*, s3_client: Any | None = None) -> int:
    """Run the image batch and return a process exit code.

    Args:
        s3_client: Optional S3 client, primarily for dependency injection.

    Returns:
        Zero for a completely successful batch execution, otherwise one.
    """
    setup_logging()

    try:
        config = load_config()
    except ConfigError as exc:
        logger.error("Configuration loading failed: %s", exc)
        return 1

    secret_source = "env-json" if config.db_secret_json else "secrets-manager"
    logger.info(
        "Starting image batch for env_name=%s secret_source=%s",
        config.env_name,
        secret_source,
    )
    try:
        if config.db_secret_json:
            secret = parse_db_secret(config.db_secret_json)
        else:
            secret = get_db_secret(config.db_secret_arn)
    except Exception as exc:
        logger.error("Database secret retrieval failed: %s", type(exc).__name__)
        return 1

    try:
        with open_connection(secret) as connection:
            with connection.cursor() as cursor:
                batch_set = find_batch_set_by_code(cursor, config.set_code)
                if batch_set is None:
                    logger.error("SET_CODE not found")
                    return 1

                try:
                    log_id = start_or_resume_execution_log(
                        cursor,
                        set_id=batch_set.id,
                        execution_arn=config.execution_arn,
                        batch_type="image_generation",
                        started_at=now_utc(),
                    )
                    connection.commit()
                except Exception as exc:
                    logger.error("Execution log start failed: %s", type(exc).__name__)
                    return 1

                if not batch_set.is_active:
                    try:
                        finalize_execution_log(
                            cursor,
                            log_id=log_id,
                            status="succeeded",
                            finished_at=now_utc(),
                            records_processed=0,
                            error_message=None,
                        )
                        connection.commit()
                        return 0
                    except Exception:
                        logger.exception("Execution log finalization failed")
                        return 1

                try:
                    generator = resolve_generator(batch_set.generator_name)
                    scheduled_at = parse_scheduled_at(config.scheduled_at)
                    generation_run_id = resolve_generation_run(
                        cursor,
                        set_id=batch_set.id,
                        scheduled_at=scheduled_at,
                    )
                    connection.commit()
                    prompt_configs = fetch_active_prompt_configs(cursor, batch_set.id)
                    if not prompt_configs:
                        raise BatchConfigError("No active prompt_configs")
                    resolved_s3_client = (
                        s3_client if s3_client is not None else boto3.client("s3")
                    )
                    result = process_prompt_configs(
                        cursor,
                        connection,
                        set_id=batch_set.id,
                        set_code=batch_set.set_code,
                        scheduled_at=scheduled_at,
                        generation_run_id=generation_run_id,
                        prompt_configs=prompt_configs,
                        generator=generator,
                        s3_bucket=config.s3_bucket_name,
                        s3_client=resolved_s3_client,
                    )
                except Exception as exc:
                    logger.exception("Image batch processing failed: %s", exc)
                    try:
                        finalize_execution_log(
                            cursor,
                            log_id=log_id,
                            status="failed",
                            finished_at=now_utc(),
                            records_processed=0,
                            error_message=str(exc),
                        )
                        connection.commit()
                    except Exception:
                        logger.exception("Execution log finalization failed")
                    return 1

                if result.all_prompt_configs_complete:
                    status = "succeeded"
                    error_message = None
                    return_code = 0
                else:
                    status = "failed"
                    error_message = "one or more prompt_configs did not complete"
                    return_code = 1

                try:
                    finalize_execution_log(
                        cursor,
                        log_id=log_id,
                        status=status,
                        finished_at=now_utc(),
                        records_processed=result.new_images_inserted,
                        error_message=error_message,
                    )
                    connection.commit()
                except Exception:
                    logger.exception("Execution log finalization failed")
                    return 1
                return return_code
    except Exception as exc:
        logger.error("Image batch database operation failed: %s", type(exc).__name__)
        return 1
