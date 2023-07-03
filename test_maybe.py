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
