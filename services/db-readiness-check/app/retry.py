"""Retry logic for waiting until the database is ready."""

from collections.abc import Callable
import logging
import time

from .db import RETRYABLE_EXCEPTIONS


logger = logging.getLogger(__name__)


def _errno(exc: BaseException) -> int | None:
    """Return a safe errno from an exception, if available."""
    if exc.args and isinstance(exc.args[0], int):
        return exc.args[0]
    return None


def wait_for_db(
    check: Callable[[], None],
    *,
    max_retries: int = 8,
    retryable: tuple[type[BaseException], ...] = RETRYABLE_EXCEPTIONS,
    sleep: Callable[[float], None] = time.sleep,
) -> bool:
    """Run a connection check until it succeeds or retries are exhausted.

    Only the supplied retryable exceptions are retried. Exception text is never
    logged because database drivers can embed sensitive connection details in it.

    Args:
        check: Callable that verifies database connectivity.
        max_retries: Number of retries after the initial attempt.
        retryable: Exception types eligible for retry.
        sleep: Sleep function used between attempts.

    Returns:
        ``True`` on success, otherwise ``False`` after retry exhaustion.
    """
    total_attempts = max_retries + 1

    for attempt in range(1, total_attempts + 1):
        logger.info("DB connection check attempt %d/%d", attempt, total_attempts)
        try:
            check()
        except retryable as exc:
            errno = _errno(exc)
            if errno is None:
                logger.warning(
                    "DB connection check failed on attempt %d/%d: %s",
                    attempt,
                    total_attempts,
                    type(exc).__name__,
                )
            else:
                logger.warning(
                    "DB connection check failed on attempt %d/%d: %s errno=%d",
                    attempt,
                    total_attempts,
                    type(exc).__name__,
                    errno,
                )

            if attempt == total_attempts:
                return False
            sleep(2.0 ** attempt)
        else:
            logger.info("DB connection check succeeded on attempt %d/%d", attempt, total_attempts)
            return True

    return False
