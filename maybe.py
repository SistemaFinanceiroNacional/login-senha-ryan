from __future__ import annotations
from typing import Generic, TypeVar, Callable, Iterable

T = TypeVar('T')
U = TypeVar('U')


class Maybe(Generic[T]):
    def map(self, function: Callable[[T], U]):
        raise NotImplementedError

    def or_else(self, default: Callable[[], T]) -> T:
        raise NotImplementedError

    def or_else_throw(self, exc) -> T:
        raise NotImplementedError

    def run(self, function: Callable[[T], None]) -> Maybe[T]:
        raise NotImplementedError


class Just(Maybe[T]):
    def __init__(self, value: T):
        self.value = value

    def map(self, function: Callable[[T], U]) -> Maybe[U]:
        return Just(function(self.value))

    def or_else(self, default: Callable[[], T]) -> T:
        return self.value

    def or_else_throw(self, exc) -> T:
        return self.value

    def run(self, function: Callable[[T], None]) -> Maybe[T]:
        function(self.value)
        return self


class Nothing(Maybe[T]):
    def map(self, function: Callable[[T], U]) -> Maybe[U]:
        return Nothing()

    def or_else(self, default: Callable[[], T]) -> T:
        return default()

    def or_else_throw(self, exc) -> T:
        raise exc

    def run(self, function: Callable[[T], None]) -> Maybe[T]:
        return self


def get_first_not_empty(possible_not_empties: Iterable[Maybe[T]]) -> Maybe[T]:
    for possible in possible_not_empties:
        if isinstance(possible, Just):
            return possible
    return Nothing()


def is_just(m: Maybe):
    return isinstance(m, Just)


def is_nothing(m: Maybe):
    return isinstance(m, Nothing)
