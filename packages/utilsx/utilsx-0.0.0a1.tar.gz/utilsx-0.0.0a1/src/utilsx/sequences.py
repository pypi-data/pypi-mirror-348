"""Utilities for working with sequences."""

from collections.abc import Sequence


def is_monotonically_growing(time_series: Sequence[float], multiplier: float) -> bool:
    """Check whether a time series can be considered monotonically growing.

    To be called so, each next element should be at least ``multiplier`` times bigger than
    a previous one. Series of less than two elements are considered non-growing.

    Args:
        time_series: A sequence of numbers.
        multiplier: How many times bigger each next element should be.

    Returns:
        True if monotonically growing, False otherwise.
    """
    if len(time_series) < 2:  # noqa: PLR2004
        return False
    return all(
        time_series[i + 1] > time_series[i] * multiplier for i in range(len(time_series) - 1)
    )
