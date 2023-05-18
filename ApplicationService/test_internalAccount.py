from ApplicationService.account import (
    Account,
    insufficientFundsException
)
from ApplicationService.transaction import create_transaction


def test_transfer1():
    t = create_transaction(1, 2, 20)
    x = Account(2, [t])
    y = 3
    x.transfer(y, 10)
    assert x.get_balance() == 10


def test_transfer_poor_ryan():
    t = create_transaction(1, 2, 10)
    x = Account(2, [t])
    y = 3
    try:
        x.transfer(y, 20)
        assert False
    except insufficientFundsException:
        assert True


def test_transactions_static_size():
    t = create_transaction(1, 2, 10)
    x = Account(2, [t])
    assert len(x._transactions) == 1


def test_transactions_incremented_size():
    t = create_transaction(1, 2, 10)
    x = Account(2, [t])
    y = 3
    x.transfer(y, 10)
    assert len(x._transactions) == 2


def test_no_balance():
    t = create_transaction(1, 2, 10)
    x = Account(2, [t])
    y = 3
    x.transfer(y, 10)
    assert x.get_balance() == 0
