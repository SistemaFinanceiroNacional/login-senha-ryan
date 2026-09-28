import math

import pytest

from domain.amount import Amount


def balance_of(bank, client) -> float:
    return bank.get_balance.execute(client.id, client.account)\
        .or_else(lambda: math.nan)


@pytest.mark.integration
def test_client_deposits_into_own_account(bank):
    alice = bank.open_client("alice")

    assert bank.deposit.execute(alice.id, alice.account, Amount(150.5))
    assert bank.deposit.execute(alice.id, alice.account, Amount(49.5))

    assert balance_of(bank, alice) == 200.0
    transactions = bank.get_transactions.execute(alice.id, alice.account)\
        .or_else(list)
    assert sorted(t.value for t in transactions) == [49.5, 150.5]


@pytest.mark.integration
def test_client_cannot_deposit_into_another_clients_account(bank):
    alice = bank.open_client("alice")
    bob = bank.open_client("bob")

    assert not bank.deposit.execute(alice.id, bob.account, Amount(100))

    assert balance_of(bank, bob) == 0.0


@pytest.mark.integration
def test_rejected_deposit_does_not_break_later_operations(bank):
    alice = bank.open_client("alice")
    bob = bank.open_client("bob")

    assert not bank.deposit.execute(alice.id, bob.account, Amount(1))

    carol = bank.open_client("carol")
    assert bank.deposit.execute(carol.id, carol.account, Amount(10))
