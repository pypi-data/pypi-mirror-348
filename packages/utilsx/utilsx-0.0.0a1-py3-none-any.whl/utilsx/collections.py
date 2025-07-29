"""Utilities for working with collections."""

from collections import Counter
from collections.abc import Iterable, Sequence, Sized
from typing import Any

from .typevars import T


def is_sequence_of_equal_elements(sequence: Sequence[Any]) -> bool:
    """Check whether all elements in a sequence are equal to each other."""
    return all(element == sequence[0] for element in sequence)


def get_duplicates(iterable: Iterable[T]) -> frozenset[T]:
    """Get a set of all values in a collection that are duplicates, i.e., present more than once.

    Args:
        iterable: A collection to check.

    Returns:
        A set of values that are present more than once.
    """
    return frozenset(key for key, value in Counter(iterable).items() if value > 1)


def check_equal_length(*collections: Sized) -> bool:
    """Given an arbitrary number of collections, check if they all have equal length."""
    if not collections:
        raise ValueError("No collections to provided to check for lengths equality.")
    benchmark_length = len(collections[0])
    return all(len(collection) == benchmark_length for collection in collections)
