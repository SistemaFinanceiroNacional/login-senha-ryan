import pytest

from domain.amount import Amount
from domain.bankaccount import (
    BankAccount,
    InsufficientFundsException
)
from domain.money import Money
from domain.transaction import create_transaction


def test_transfer1():
    t = create_transaction(1, 2, Amount(20))
    x = BankAccount(2, [t])
    y = 3
    x.transfer(y, Amount(10))
    assert x.get_balance() == Money(10)


def test_transfer_poor_ryan():
    t = create_transaction(1, 2, Amount(10))
    x = BankAccount(2, [t])
    y = 3
    with pytest.raises(InsufficientFundsException):
        x.transfer(y, Amount(20))


def test_transactions_static_size():
    t = create_transaction(1, 2, Amount(10))
    x = BankAccount(2, [t])
    assert len(x._transactions) == 1


def test_transactions_incremented_size():
    t = create_transaction(1, 2, Amount(10))
    x = BankAccount(2, [t])
    y = 3
    x.transfer(y, Amount(10))
    assert len(x._transactions) == 2


def test_no_balance():
    t = create_transaction(1, 2, Amount(10))
    x = BankAccount(2, [t])
    y = 3
    x.transfer(y, Amount(10))
    assert x.get_balance() == Money(0)


def test_balance_is_exact_to_the_cent():
    account = BankAccount(2, [])

    for _ in range(3):
        account.deposit(Amount("0.10"))

    assert account.get_balance() == Money("0.30")
