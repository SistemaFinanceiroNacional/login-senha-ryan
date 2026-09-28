from typing import Callable, TypeVar

from maybe import Maybe, Just, Nothing

T = TypeVar("T")


def _parse(convert: Callable[[str], T], raw) -> Maybe[T]:
    try:
        return Just(convert(raw))
    except (TypeError, ValueError):
        return Nothing()


def parse_int(raw) -> Maybe[int]:
    return _parse(int, raw)


def parse_float(raw) -> Maybe[float]:
    return _parse(float, raw)
