import pytest

import maybe


@pytest.mark.getFirstNotEmpty
def test_nothing():
    possible = maybe.getFirstNotEmpty([])
    assert isinstance(possible, maybe.nothing)


@pytest.mark.getFirstNotEmpty
def test_list_of_nothings():
    possible = maybe.getFirstNotEmpty(
        [
            maybe.nothing(),
            maybe.nothing(),
            maybe.nothing()
        ]
    )
    assert isinstance(possible, maybe.nothing)


@pytest.mark.getFirstNotEmpty
def test_one_just():
    possible = maybe.getFirstNotEmpty(
        [
            maybe.nothing(),
            maybe.nothing(),
            maybe.just(3)
        ]
    )
    assert isinstance(possible, maybe.just)


@pytest.mark.getFirstNotEmpty
def test_two_just():
    possible = maybe.getFirstNotEmpty(
        [
            maybe.nothing(),
            maybe.just(10),
            maybe.just(3)
        ]
    )
    assert isinstance(possible, maybe.just) and possible.value == 10
