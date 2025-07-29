from collections.abc import Collection
from typing import Any

import pytest

from utilsx import sort_by_value, sum_dicts


@pytest.mark.parametrize(
    ("dictionary", "reverse", "output"),
    (
        ({"a": 1, "b": 2}, True, {"b": 2, "a": 1}),
        ({False: 1, True: 2}, True, {True: 2, False: 1}),
        ({"a": 1, "b": 3, "c": 2}, False, {"a": 1, "c": 2, "b": 3}),
        ({"a": 1}, False, {"a": 1}),
        ({"a": 1}, True, {"a": 1}),
        ({}, True, {}),
    ),
)
def test_sort_by_value(
    dictionary: dict[Any, float],
    reverse: bool,
    output: dict[Any, float],
) -> None:
    assert tuple(sort_by_value(dictionary, reverse)) == tuple(output)


@pytest.mark.parametrize(
    ("inputs", "output"),
    (
        (({"a": 1, "b": 2}, {"c": 3}), {"a": 1, "b": 2, "c": 3}),
        (({"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3}), {"a": 2, "b": 4, "c": 3}),
        (({}, {}), {}),
        (({"a": 1},) * 3, {"a": 3}),
    ),
)
def test_sum_dicts(
    inputs: Collection[dict[Any, float]],
    output: dict[Any, float],
) -> None:
    assert sum_dicts(*inputs) == output
