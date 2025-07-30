"""Configures structured, colored, and optionally file-based logging using Loguru."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from sys import stderr

import loguru
from loguru import logger

SCAN_LOGGER_ROTATION = "500 MB"
LOGGER_FILE_FORMAT = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
LOGGER_FILENAME = "netwatcher-{time:YYYY-MM-DD-HH-mm-ss}.log"


class Verbosity(str, Enum):
    """Log verbosity levels mapped to Loguru's level names."""

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    @classmethod
    def from_count(cls, count: int) -> Verbosity:
        """Derive verbosity level from count of `-v` flags.

        Args:
            count (int): Number of times `-v` is passed on the command line.

        Returns:
            Verbosity: The appropriate verbosity level, capped at the most verbose.
        """
        levels = [
            cls.CRITICAL,
            cls.ERROR,
            cls.WARNING,
            cls.INFO,
            cls.DEBUG,
            cls.TRACE,
        ]
        index = min(count, len(levels) - 1)
        return levels[index]


def stderr_fmt(record: loguru.Record) -> str:
    """Return a dynamic log format string based on the severity of the log record.

    Args:
        record (loguru.Record): A Loguru log record.

    Returns:
        str: A colorized and structured log format string.
    """
    if record["level"].no >= 40:
        return "<green>{time}</> - {level} - <red>{thread}</> - <lvl>{message}</>\n{exception}"
    else:
        return "<green>{time}</> - {level} - <lvl>{message}</lvl>\n{exception}"


def setup_logging(log_dir: Path | None = None, verbose: int = 1) -> None:
    """Configure Loguru logging with optional file logging.

    This sets up a stderr sink with dynamic formatting and optional structured file logging
    with rotation and JSON serialization.

    Args:
        log_dir (Path | None, optional): Optional directory location for which to write a log file. Defaults to `None`.
        verbose (int, optional): Verbosity level (-v, -vv, -vvv). Defaults to 0.
    """
    logger.remove()
    level = Verbosity.from_count(verbose).value
    logger.add(sink=stderr, format=stderr_fmt, colorize=True, level=level, backtrace=True, diagnose=True, enqueue=True)

    if log_dir is not None:
        sink = log_dir.joinpath(LOGGER_FILENAME).resolve()
        logger.add(
            sink=sink,
            level=level,
            format=LOGGER_FILE_FORMAT,
            serialize=True,
            backtrace=True,
            diagnose=True,
            rotation=SCAN_LOGGER_ROTATION,
            enqueue=True,
        )
