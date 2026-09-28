import math

import pytest

NOT_IMPLEMENTED = "deposit not implemented yet (issue #110)"


def balance_of(bank, account) -> float:
    return bank.get_balance.execute(account).or_else(lambda: math.nan)


@pytest.mark.integration
@pytest.mark.xfail(strict=True, reason=NOT_IMPLEMENTED,
                   raises=NotImplementedError)
def test_client_deposits_into_own_account(bank):
    alice = bank.open_client("alice")

    assert bank.deposit.execute(alice.id, alice.account, 150.5)
    assert bank.deposit.execute(alice.id, alice.account, 49.5)

    assert balance_of(bank, alice.account) == 200.0
    transactions = bank.get_transactions.execute(alice.account)\
        .or_else(list)
    assert sorted(t.value for t in transactions) == [49.5, 150.5]


@pytest.mark.integration
@pytest.mark.xfail(strict=True, reason=NOT_IMPLEMENTED,
                   raises=NotImplementedError)
def test_client_cannot_deposit_into_another_clients_account(bank):
    alice = bank.open_client("alice")
    bob = bank.open_client("bob")

    assert not bank.deposit.execute(alice.id, bob.account, 100.0)

    assert balance_of(bank, bob.account) == 0.0


@pytest.mark.integration
@pytest.mark.xfail(strict=True, reason=NOT_IMPLEMENTED,
                   raises=NotImplementedError)
@pytest.mark.parametrize("amount", [0, -10, math.nan, math.inf])
def test_invalid_amounts_are_not_deposited(bank, amount):
    alice = bank.open_client("alice")

    assert not bank.deposit.execute(alice.id, alice.account, amount)

    assert balance_of(bank, alice.account) == 0.0


@pytest.mark.integration
@pytest.mark.xfail(strict=True, reason=NOT_IMPLEMENTED,
                   raises=NotImplementedError)
def test_rejected_deposit_does_not_break_later_operations(bank):
    alice = bank.open_client("alice")

    assert not bank.deposit.execute(alice.id, alice.account, -1)

    bob = bank.open_client("bob")
    assert bank.deposit.execute(bob.id, bob.account, 10.0)
