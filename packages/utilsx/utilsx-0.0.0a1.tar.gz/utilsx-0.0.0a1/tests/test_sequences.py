import pytest

from utilsx import is_monotonically_growing


@pytest.mark.parametrize(
    ("time_series", "known_answer"),
    (
        ((1,), False),
        ((1, 2), True),
        ((1, 2, 3), True),
        ((1, 1.2, 1.5), True),
        ((1, 2, 2), False),
        ((1, 1.01, 1.02), False),
        ((1, 2, 3, 4, 5, 1), False),
    ),
)
def test_is_monotonically_growing(
    time_series: tuple[float],
    known_answer: bool,
) -> None:
    assert is_monotonically_growing(time_series, 1.1) == known_answer
