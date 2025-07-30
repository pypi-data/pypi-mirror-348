"""Unit tests for the custom logging configuration module."""

from netwatcher.logging_config import Verbosity


def test_verbosity_from_count() -> None:
    """Test that Verbosity.from_count maps flag counts to correct log levels."""
    assert Verbosity.from_count(0) == Verbosity.CRITICAL
    assert Verbosity.from_count(1) == Verbosity.ERROR
    assert Verbosity.from_count(2) == Verbosity.WARNING
    assert Verbosity.from_count(3) == Verbosity.INFO
    assert Verbosity.from_count(4) == Verbosity.DEBUG
    assert Verbosity.from_count(5) == Verbosity.TRACE
    assert Verbosity.from_count(100) == Verbosity.TRACE  # Cap at max level
