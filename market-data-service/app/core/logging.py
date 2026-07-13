import sys

from loguru import logger

from app.core.config import settings


def configure_logging() -> None:
    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level}</level> | "
            "{name}:{function}:{line} | "
            "<cyan>{message}</cyan>"
        ),
    )