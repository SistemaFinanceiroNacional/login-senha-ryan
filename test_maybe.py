import maybe

def test_getFirstNotEmpty_nothing():
    possible = maybe.getFirstNotEmpty([])
    assert isinstance(possible, maybe.nothing)

def test_getFirstNotEmpty_list_of_nothings():
    possible = maybe.getFirstNotEmpty([maybe.nothing(), maybe.nothing(), maybe.nothing()])
    assert isinstance(possible, maybe.nothing)

def test_getFirstNotEmpty_one_just():
    possible = maybe.getFirstNotEmpty([maybe.nothing(), maybe.nothing(), maybe.just(3)])
    assert isinstance(possible, maybe.just)

def test_getFirstNotEmpty_two_just():
    possible = maybe.getFirstNotEmpty([maybe.nothing(), maybe.just(10), maybe.just(3)])
    assert possible.value == 10