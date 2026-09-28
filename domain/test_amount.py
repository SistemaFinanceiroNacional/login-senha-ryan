import math

import pytest

from domain.amount import Amount, InvalidAmount


@pytest.mark.parametrize("value", [0.01, 1, 150.5])
def test_positive_finite_values_are_amounts(value):
    assert Amount(value).to_float() == value


@pytest.mark.parametrize("value", [0, -0.01, -10, math.nan, math.inf,
                                   -math.inf])
def test_other_values_are_not_amounts(value):
    with pytest.raises(InvalidAmount):
        Amount(value)


def test_amounts_are_compared_by_value():
    assert Amount(10) == Amount(10.0)
    assert Amount(10) != Amount(20)
    assert len({Amount(10), Amount(10.0)}) == 1
