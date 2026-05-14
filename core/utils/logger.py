"""
logger.py
=========

Central logging utility for the entire project.

Features:
- DEBUG / INFO logs shown in console
- Consistent format across all modules
- Safe against duplicate handlers
- Module-level logger support

Usage:
    from utils.logger import get_logger
    logger = get_logger(__name__)
"""

import logging
import sys
from typing import Optional

# Default log format
LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-5s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Internal flag to avoid re-configuring logging multiple times
_LOGGING_CONFIGURED = False


def _configure_root_logger(level: int = logging.DEBUG) -> None:
    """
    Configure root logger once for the entire application.
    """
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

    _LOGGING_CONFIGURED = True


def get_logger(
    name: Optional[str] = None,
    level: int = logging.DEBUG
) -> logging.Logger:
    """
    Returns a configured logger for a module.

    Args:
        name: Usually __name__
        level: Logging level (DEBUG, INFO, etc.)

    Returns:
        logging.Logger
    """
    _configure_root_logger(level)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger