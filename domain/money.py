from __future__ import annotations

from decimal import Decimal, InvalidOperation
from functools import total_ordering
from typing import Union

CENT = Decimal("0.01")

MoneyValue = Union[Decimal, int, str]


class InvalidMoney(Exception):
    def __init__(self, value):
        super().__init__(f"{value!r} is not a valid amount of money.")


def _to_cents(value: MoneyValue) -> Decimal:
    if isinstance(value, (float, bool)):
        raise TypeError(
            f"{value!r}: money is built from Decimal, int or str, never "
            f"from binary floating point"
        )
    try:
        decimal = Decimal(value)
        cents = decimal.quantize(CENT)
    except (InvalidOperation, TypeError, ValueError):
        raise InvalidMoney(value)
    if not decimal.is_finite() or cents != decimal:
        raise InvalidMoney(value)
    return cents


@total_ordering
class Money:
    """A quantity of money, exact to the cent. It may be zero or negative,
    e.g. a balance."""

    __slots__ = ("_cents",)

    def __init__(self, value: MoneyValue):
        self._cents = _to_cents(value)

    @classmethod
    def zero(cls) -> Money:
        return Money(0)

    def to_decimal(self) -> Decimal:
        return self._cents

    def __add__(self, other: Money) -> Money:
        return Money(self._cents + other._cents)

    def __sub__(self, other: Money) -> Money:
        return Money(self._cents - other._cents)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Money) and self._cents == other._cents

    def __lt__(self, other: Money) -> bool:
        return self._cents < other._cents

    def __hash__(self) -> int:
        return hash(self._cents)

    def __str__(self) -> str:
        return f"{self._cents:.2f}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"
