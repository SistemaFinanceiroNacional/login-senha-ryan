from typing import Callable, TypeVar

from domain.amount import Amount
from domain.money import InvalidMoney
from maybe import Maybe, Just, Nothing

T = TypeVar("T")


def _parse(convert: Callable[[str], T], raw) -> Maybe[T]:
    try:
        return Just(convert(raw))
    except (TypeError, ValueError, InvalidMoney):
        return Nothing()


def parse_int(raw) -> Maybe[int]:
    return _parse(int, raw)


def parse_amount(raw) -> Maybe[Amount]:
    return _parse(Amount, raw)
