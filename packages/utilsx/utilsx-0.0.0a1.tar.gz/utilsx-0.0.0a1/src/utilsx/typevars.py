"""A collection of type variables."""

from typing import TypeVar

# Unbounded, unconstrained TypeVar to be used wherever input-output type match is needed.
T = TypeVar("T")

# TypeVar bounded to float, i.e., also includes int.
NumberT = TypeVar("NumberT", bound=float)
