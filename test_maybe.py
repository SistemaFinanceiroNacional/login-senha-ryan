import pytest
import maybe


@pytest.mark.get_first_not_empty
def test_nothing():
    possible = maybe.get_first_not_empty([])
    assert isinstance(possible, maybe.Nothing)


@pytest.mark.get_first_not_empty
def test_list_of_nothings():
    possible = maybe.get_first_not_empty(
        [
            maybe.Nothing(),
            maybe.Nothing(),
            maybe.Nothing()
        ]
    )
    assert isinstance(possible, maybe.Nothing)


@pytest.mark.get_first_not_empty
def test_one_just():
    possible = maybe.get_first_not_empty(
        [
            maybe.Nothing(),
            maybe.Nothing(),
            maybe.Just(3)
        ]
    )
    assert isinstance(possible, maybe.Just)


@pytest.mark.get_first_not_empty
def test_two_just():
    possible = maybe.get_first_not_empty(
        [
            maybe.Nothing(),
            maybe.Just(10),
            maybe.Just(3)
        ]
    )
    assert isinstance(possible, maybe.Just) and possible.value == 10
