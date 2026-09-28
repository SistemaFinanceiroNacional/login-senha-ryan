import pytest

from domain.amount import Amount
from maybe import is_nothing


@pytest.fixture
def alice(bank):
    alice = bank.open_client("alice")
    assert bank.deposit.execute(alice.id, alice.account, Amount(100))
    return alice


@pytest.fixture
def bob(bank):
    bob = bank.open_client("bob")
    assert bank.deposit.execute(bob.id, bob.account, Amount(500))
    return bob


@pytest.mark.integration
def test_client_gets_balance_of_own_account(bank, alice):
    balance = bank.get_balance.execute(
        alice.id, alice.account
    )

    assert balance.or_else(lambda: 0.0) == 100.0


@pytest.mark.integration
def test_client_does_not_get_balance_of_another_clients_account(
        bank, alice, bob
):
    balance = bank.get_balance.execute(
        alice.id, bob.account
    )

    assert is_nothing(balance)


@pytest.mark.integration
def test_client_gets_transactions_of_own_account(bank, alice):
    transactions = bank.get_transactions.execute(
        alice.id, alice.account
    )

    assert [t.value for t in transactions.or_else(list)] == [100.0]


@pytest.mark.integration
def test_client_does_not_get_transactions_of_another_clients_account(
        bank, alice, bob
):
    transactions = bank.get_transactions.execute(
        alice.id, bob.account
    )

    assert is_nothing(transactions)
