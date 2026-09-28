from decimal import Decimal

import pytest

from domain.money import InvalidMoney, Money


@pytest.mark.parametrize("value", ["0.10", Decimal("0.1"), "7", 7, "-3.25"])
def test_money_is_built_from_exact_values(value):
    assert Money(value).to_decimal() == Decimal(value)


@pytest.mark.parametrize("value", [0.1, 10.0, True])
def test_money_is_never_built_from_floats(value):
    with pytest.raises(TypeError):
        Money(value)


@pytest.mark.parametrize("value", ["abc", "", "nan", "inf", "-Infinity",
                                   "0.001", "1e-3", None])
def test_invalid_values_are_not_money(value):
    with pytest.raises(InvalidMoney):
        Money(value)


def test_cents_add_up_exactly():
    total = Money("0.10") + Money("0.10") + Money("0.10")

    assert total == Money("0.30")
    assert str(total) == "0.30"


def test_money_can_become_negative():
    assert Money("1.00") - Money("2.50") == Money("-1.50")


def test_money_is_compared_by_value():
    assert Money("10") == Money("10.00")
    assert Money("9.99") < Money("10")
    assert Money("10") >= Money("10.00")
    assert len({Money("10"), Money("10.00")}) == 1


def test_money_is_shown_with_two_decimal_places():
    assert str(Money(7)) == "7.00"
    assert str(Money.zero()) == "0.00"
    assert repr(Money("7.5")) == "Money('7.50')"
