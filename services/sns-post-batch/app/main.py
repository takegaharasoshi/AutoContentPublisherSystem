"""SNS posting batch application orchestration and logging setup."""

from __future__ import annotations

import logging
import sys
from typing import Any
import urllib.request

import boto3

from acps_shared.db import open_connection
from acps_shared.secrets import get_db_secret, parse_db_secret

from .batch_sets import find_batch_set_by_code
from .caption_templates import fetch_active_caption_template
from .clock import now_utc
from .config import ConfigError, load_config
from .execution_log import finalize_execution_log, start_or_resume_execution_log
from .generated_images import fetch_first_generated_image
from .processing import process_target_generation_run
from .sns_accounts import fetch_active_sns_accounts
from .target_selection import resolve_target_generation_run


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure stdout logging for the ECS awslogs log driver."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )


def main(*, s3_client: Any | None = None, urlopen: Any | None = None) -> int:
    """Run the SNS posting batch and return a process exit code.

    Args:
        s3_client: Optional S3 client used for presigned URLs.
        urlopen: Optional HTTP opener used by the Instagram API client.

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
        "Starting SNS posting batch for env_name=%s secret_source=%s",
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
                        batch_type="sns_posting",
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
                    generation_run_id = resolve_target_generation_run(
                        cursor, batch_set.id
                    )
                    if generation_run_id is None:
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

                    sns_accounts = fetch_active_sns_accounts(cursor, batch_set.id)
                    caption_template = fetch_active_caption_template(
                        cursor, batch_set.id
                    )
                    generated_image = fetch_first_generated_image(
                        cursor, generation_run_id
                    )
                    if generated_image is None:
                        raise RuntimeError(
                            "No generated image was found for the target generation run"
                        )

                    resolved_s3_client = (
                        s3_client if s3_client is not None else boto3.client("s3")
                    )
                    resolved_urlopen = (
                        urlopen if urlopen is not None else urllib.request.urlopen
                    )
                    result = process_target_generation_run(
                        cursor,
                        connection,
                        set_id=batch_set.id,
                        generation_run_id=generation_run_id,
                        sns_accounts=sns_accounts,
                        caption_template=caption_template,
                        generated_image=generated_image,
                        env_name=config.env_name,
                        set_code=batch_set.set_code,
                        s3_bucket=config.s3_bucket_name,
                        s3_client=resolved_s3_client,
                        urlopen=resolved_urlopen,
                    )
                except Exception as exc:
                    logger.exception("SNS posting batch processing failed: %s", exc)
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

                if result.all_accounts_success:
                    status = "succeeded"
                    error_message = None
                    return_code = 0
                else:
                    status = "failed"
                    error_message = "one or more sns_accounts did not reach success"
                    return_code = 1

                try:
                    finalize_execution_log(
                        cursor,
                        log_id=log_id,
                        status=status,
                        finished_at=now_utc(),
                        records_processed=result.accounts_processed,
                        error_message=error_message,
                    )
                    connection.commit()
                except Exception:
                    logger.exception("Execution log finalization failed")
                    return 1
                return return_code
    except Exception as exc:
        logger.error(
            "SNS posting batch database operation failed: %s", type(exc).__name__
        )
        return 1
