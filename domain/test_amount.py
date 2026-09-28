from decimal import Decimal

import pytest

from domain.amount import Amount, InvalidAmount
from domain.money import InvalidMoney, Money


@pytest.mark.parametrize("value", ["0.01", 1, "150.50", Decimal("7.5")])
def test_positive_values_are_amounts(value):
    assert Amount(value).to_decimal() == Decimal(value)


@pytest.mark.parametrize("value", [0, "0.00", "-0.01", -10, "nan", "inf",
                                   "0.001", "abc"])
def test_other_values_are_not_amounts(value):
    with pytest.raises(InvalidAmount):
        Amount(value)


def test_an_invalid_amount_is_invalid_money():
    with pytest.raises(InvalidMoney):
        Amount(0)


def test_amounts_are_never_built_from_floats():
    with pytest.raises(TypeError):
        Amount(10.0)  # type: ignore[arg-type]


def test_an_amount_is_money():
    assert Amount("10") == Money("10.00")
    assert Money("5") + Amount("0.10") == Money("5.10")
