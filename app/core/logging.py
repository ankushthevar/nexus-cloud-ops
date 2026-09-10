import logging
import sys

from app.core.config import get_settings


def setup_logging() -> None:
    settings = get_settings()

    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()

    root_logger.setLevel(log_level)

    # Prevent duplicate handlers when reloading during development.
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)