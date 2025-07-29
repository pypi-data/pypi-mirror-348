"""Utilities for working with charts, be it the UI app of just one-off EDA."""

import math
from collections.abc import Sized

__all__ = ["find_optimal_nbins"]


def find_optimal_nbins(values: Sized) -> int:
    """Find the optimal number of bins to represent values as a histogram.

    Uses "The square root choice" algorithm, which is the default in MS Excel.

    Args:
        values: Array of values.

    Returns:
        The optimal number of bins to represent those as a histogram.
    """
    return int(math.sqrt(len(values)))
