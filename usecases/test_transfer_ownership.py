import pytest

from domain.amount import Amount
from domain.money import Money
from usecases.contexterrors.businesserror import BusinessError
from usecases.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.xfail(strict=True, raises=TypeError,
                      reason="transfers do not know who asks (issue #107)"),
]


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


def balance(bank, client) -> Money:
    return bank.get_balance.execute(client.id, client.account)\
        .or_else_throw(AssertionError("no balance"))


def test_a_client_transfers_from_their_own_account(bank, alice, bob):
    assert bank.transfer.execute(alice.id, alice.account, bob.account,
                                 Amount(30))

    assert balance(bank, alice) == Money(70)
    assert balance(bank, bob) == Money(530)


def test_a_client_cannot_transfer_from_someone_elses_account(
        bank, alice, bob
):
    with pytest.raises(AccountDoesNotExistsError):
        bank.transfer.execute(alice.id, bob.account, alice.account,
                              Amount(300))

    assert balance(bank, bob) == Money(500)
    assert balance(bank, alice) == Money(100)


def test_an_account_cannot_transfer_to_itself(bank, alice):
    with pytest.raises(BusinessError):
        bank.transfer.execute(alice.id, alice.account, alice.account,
                              Amount(10))

    assert balance(bank, alice) == Money(100)
