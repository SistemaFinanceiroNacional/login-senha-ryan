from typing import Any

import pytest
from maybe import Maybe, Just, Nothing, get_first_not_empty


@pytest.mark.get_first_not_empty
def test_nothing():
    possible: Maybe[Any] = get_first_not_empty([])
    assert isinstance(possible, Nothing)


@pytest.mark.get_first_not_empty
def test_list_of_nothings():
    possible: Maybe[Any] = get_first_not_empty(
        [
            Nothing(),
            Nothing(),
            Nothing()
        ]
    )
    assert isinstance(possible, Nothing)


@pytest.mark.get_first_not_empty
def test_one_just():
    possible: Maybe[Any] = get_first_not_empty(
        [
            Nothing(),
            Nothing(),
            Just(3)
        ]
    )
    assert isinstance(possible, Just)


@pytest.mark.get_first_not_empty
def test_two_just():
    possible: Maybe[Any] = get_first_not_empty(
        [
            Nothing(),
            Just(10),
            Just(3)
        ]
    )
    assert isinstance(possible, Just) and possible.value == 10


def half(number: int) -> Maybe[int]:
    if number % 2 == 0:
        return Just(number // 2)
    return Nothing()


def test_flat_map_on_just_returns_the_function_result():
    assert Just(10).flat_map(half).or_else(lambda: -1) == 5
    assert isinstance(Just(3).flat_map(half), Nothing)


def test_flat_map_on_nothing_does_not_call_the_function():
    def fail(_):
        raise AssertionError("must not be called")

    assert isinstance(Nothing().flat_map(fail), Nothing)


def test_nothing_is_returned_as_is_by_map_and_flat_map():
    nothing: Maybe[int] = Nothing()

    assert nothing.map(lambda number: number + 1) is nothing
    assert nothing.flat_map(half) is nothing
