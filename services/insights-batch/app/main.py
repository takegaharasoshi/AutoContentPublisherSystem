"""Insights collection batch orchestration and logging setup."""

from __future__ import annotations

import logging
import sys
from typing import Any
import urllib.request

from acps_shared.db import open_connection
from acps_shared.secrets import get_db_secret, parse_db_secret

from .batch_sets import find_batch_set_by_code
from .clock import now_utc, parse_scheduled_at
from .config import ConfigError, load_config
from .execution_log import finalize_execution_log, start_or_resume_execution_log
from .processing import process_accounts
from .sns_accounts import fetch_active_sns_accounts


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure stdout logging for the ECS awslogs log driver."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )


def main(*, secrets_client: Any | None = None, urlopen: Any | None = None) -> int:
    """Run the insights collection batch and return a process exit code."""
    setup_logging()
    try:
        config = load_config()
    except ConfigError as exc:
        logger.error("Configuration loading failed: %s", exc)
        return 1

    secret_source = "env-json" if config.db_secret_json else "secrets-manager"
    logger.info(
        "Starting insights collection batch for env_name=%s secret_source=%s",
        config.env_name,
        secret_source,
    )
    try:
        secret = (
            parse_db_secret(config.db_secret_json)
            if config.db_secret_json
            else get_db_secret(config.db_secret_arn)
        )
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
                        batch_type="insights_collection",
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
                    scheduled_at = parse_scheduled_at(config.scheduled_at)
                    accounts = fetch_active_sns_accounts(cursor, batch_set.id)
                    result = process_accounts(
                        cursor,
                        connection,
                        set_id=batch_set.id,
                        accounts=accounts,
                        env_name=config.env_name,
                        set_code=batch_set.set_code,
                        scheduled_at=scheduled_at,
                        media_lookback_days=config.media_lookback_days,
                        secrets_client=secrets_client,
                        urlopen=(
                            urlopen if urlopen is not None else urllib.request.urlopen
                        ),
                    )
                except Exception as exc:
                    logger.exception(
                        "Insights collection batch processing failed: error_type=%s",
                        type(exc).__name__,
                    )
                    try:
                        finalize_execution_log(
                            cursor,
                            log_id=log_id,
                            status="failed",
                            finished_at=now_utc(),
                            records_processed=0,
                            error_message=type(exc).__name__,
                        )
                        connection.commit()
                    except Exception:
                        logger.exception("Execution log finalization failed")
                    return 1

                if result.failure_count == 0:
                    status = "succeeded"
                    error_message = None
                    return_code = 0
                else:
                    status = "failed"
                    error_message = (
                        f"insights collection failures: {result.failure_count}"
                    )
                    return_code = 1
                try:
                    finalize_execution_log(
                        cursor,
                        log_id=log_id,
                        status=status,
                        finished_at=now_utc(),
                        records_processed=result.records_inserted,
                        error_message=error_message,
                    )
                    connection.commit()
                except Exception:
                    logger.exception("Execution log finalization failed")
                    return 1
                return return_code
    except Exception as exc:
        logger.error(
            "Insights collection batch database operation failed: %s",
            type(exc).__name__,
        )
        return 1
