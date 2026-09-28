from __future__ import annotations

import math


class InvalidAmount(Exception):
    def __init__(self, value):
        super().__init__(f"{value!r} is not a valid amount of money.")


class Amount:
    """A quantity of money moved by an operation (a deposit, a transfer):
    always positive and finite. Invalid values cannot be represented."""

    __slots__ = ("_value",)

    def __init__(self, value: float):
        if not (math.isfinite(value) and value > 0):
            raise InvalidAmount(value)
        self._value = value

    def to_float(self) -> float:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Amount) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Amount({self._value!r})"
