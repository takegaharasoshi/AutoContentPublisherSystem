"""Application orchestration and logging setup."""

import logging
import sys

from acps_shared.db import open_connection
from acps_shared.secrets import get_db_secret, parse_db_secret

from .config import ConfigError, load_config


SERVICE_NAME = "sns-post-batch"

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure stdout logging for the ECS awslogs log driver."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )


def main() -> int:
    """Run the database connection test and return a process exit code."""
    setup_logging()

    try:
        config = load_config()
    except ConfigError as exc:
        # ConfigError のメッセージは環境変数名のみで Secret 値を含まないため出力してよい
        logger.error("Configuration loading failed: %s", exc)
        return 1

    secret_source = "env-json" if config.db_secret_json else "secrets-manager"
    logger.info(
        "Starting DB connection test for env_name=%s secret_source=%s",
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
                cursor.execute(
                    "INSERT INTO connection_test (service_name) VALUES (%s)",
                    (SERVICE_NAME,),
                )
                inserted_id = cursor.lastrowid
            connection.commit()

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM connection_test")
                row_count = cursor.fetchone()[0]
    except Exception as exc:
        logger.error("DB 接続テスト失敗: %s", type(exc).__name__)
        return 1

    logger.info(
        "DB 接続成功: connection_test への INSERT/SELECT を確認しました "
        "(service_name=%s, inserted_id=%s, row_count=%s)",
        SERVICE_NAME,
        inserted_id,
        row_count,
    )
    return 0
