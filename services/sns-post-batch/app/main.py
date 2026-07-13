"""Application orchestration and logging setup."""

import logging
import sys


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure stdout logging for the ECS awslogs log driver."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )


def main() -> int:
    """Run the Phase 4 dry-run batch and return a process exit code."""
    setup_logging()
    logger.info("Hello World from sns-post-batch")
    return 0
