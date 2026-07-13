"""Application orchestration and logging setup."""

from functools import partial
import logging
import sys

from .config import ConfigError, load_config
from .db import check_connection
from .retry import wait_for_db
from .secrets import get_db_secret


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure stdout logging for the ECS awslogs log driver."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )


def main() -> int:
    """Run the DB readiness check and return a process exit code."""
    setup_logging()

    try:
        config = load_config()
    except ConfigError as exc:
        # ConfigError のメッセージは環境変数名のみで Secret 値を含まないため出力してよい
        logger.error("Configuration loading failed: %s", exc)
        return 1

    logger.info(
        "Starting DB readiness check for env_name=%s secret_arn=%s",
        config.env_name,
        config.db_secret_arn,
    )

    try:
        secret = get_db_secret(config.db_secret_arn)
    except Exception as exc:
        logger.error("Database secret retrieval failed: %s", type(exc).__name__)
        return 1

    try:
        ready = wait_for_db(partial(check_connection, secret))
    except Exception as exc:
        logger.error("Database readiness check failed: %s", type(exc).__name__)
        return 1

    if ready:
        logger.info("Database is ready")
        return 0

    logger.error("Database did not become ready before retries were exhausted")
    return 1
