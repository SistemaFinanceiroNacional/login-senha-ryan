import pytest

from domain.amount import Amount
from domain.bankaccount import InsufficientFundsException

pytestmark = pytest.mark.integration


def test_a_failed_operation_does_not_taint_the_following_ones(bank):
    alice = bank.open_client("alice")
    bob = bank.open_client("bob")
    with pytest.raises(InsufficientFundsException):
        bank.transfer.execute(alice.id, alice.account, bob.account,
                              Amount(10))

    assert bank.new_bank_account.execute(alice.id)
    assert bank.deposit.execute(alice.id, alice.account, Amount(50))
    assert bank.transfer.execute(alice.id, alice.account, bob.account,
                                 Amount(10))
