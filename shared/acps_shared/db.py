"""Database connection helpers."""

from collections.abc import Iterator
from contextlib import contextmanager

import pymysql

from .secrets import DbSecret


def connect(
    secret: DbSecret, connect_timeout: int = 10
) -> pymysql.connections.Connection:
    """Open a database connection using the supplied secret.

    Connection retries are the responsibility of the database readiness check
    task (db-readiness-check); this module does not retry connections.

    Args:
        secret: Database connection parameters.
        connect_timeout: Connection timeout in seconds.

    Returns:
        An open PyMySQL connection.

    Raises:
        pymysql.MySQLError: If the connection fails.
    """
    return pymysql.connect(
        host=secret.host,
        port=secret.port,
        user=secret.username,
        password=secret.password,
        database=secret.dbname,
        connect_timeout=connect_timeout,
        charset="utf8mb4",
    )


@contextmanager
def open_connection(
    secret: DbSecret, connect_timeout: int = 10
) -> Iterator[pymysql.connections.Connection]:
    """Open a database connection and close it when the context exits.

    Connection retries are the responsibility of the database readiness check
    task (db-readiness-check); this module does not retry connections.

    Args:
        secret: Database connection parameters.
        connect_timeout: Connection timeout in seconds.

    Yields:
        An open PyMySQL connection.
    """
    connection = connect(secret, connect_timeout=connect_timeout)
    try:
        yield connection
    finally:
        connection.close()
