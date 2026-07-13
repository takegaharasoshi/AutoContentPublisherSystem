"""Database connection check implementation."""

import pymysql

from .secrets import DbSecret


RETRYABLE_EXCEPTIONS = (pymysql.err.OperationalError, pymysql.err.InterfaceError)


def check_connection(secret: DbSecret, connect_timeout: int = 10) -> None:
    """Connect to the database and run a minimal query.

    Args:
        secret: Database connection parameters.
        connect_timeout: Connection timeout in seconds.

    Raises:
        pymysql.MySQLError: If the connection or query fails.
    """
    connection = pymysql.connect(
        host=secret.host,
        port=secret.port,
        user=secret.username,
        password=secret.password,
        database=secret.dbname,
        connect_timeout=connect_timeout,
    )
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
    finally:
        connection.close()
