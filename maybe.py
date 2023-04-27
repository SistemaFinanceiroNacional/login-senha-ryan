from typing import Generic, TypeVar, Callable, Iterable

T = TypeVar('T')
U = TypeVar('U')


class maybe(Generic[T]):
    def map(self, function: Callable[[T], U]):
        raise NotImplementedError

    def orElse(self, default: Callable[[], T]) -> T:
        raise NotImplementedError

    def orElseThrow(self, exc) -> T:
        raise NotImplementedError


class just(maybe[T]):
    def __init__(self, value: T):
        self.value = value

    def map(self, function: Callable[[T], U]) -> maybe[U]:
        return just(function(self.value))

    def orElse(self, default: Callable[[], T]) -> T:
        return self.value

    def orElseThrow(self, exc) -> None:
        return self.value


class nothing(maybe[T]):
    def map(self, function: Callable[[T], U]) -> maybe[U]:
        return self

    def orElse(self, default: Callable[[], T]) -> T:
        return default()

    def orElseThrow(self, exc) -> None:
        raise exc


def getFirstNotEmpty(possible_not_empties: Iterable[maybe[T]]) -> maybe[T]:
    for possible in possible_not_empties:
        if isinstance(possible, just):
            return possible
    return nothing()
