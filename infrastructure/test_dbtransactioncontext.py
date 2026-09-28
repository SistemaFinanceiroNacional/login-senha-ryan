import pytest

from domain.amount import Amount
from domain.bankaccount import InsufficientFundsException
from testsupport.bank import PASSWORD

pytestmark = pytest.mark.integration


def test_a_failed_operation_does_not_taint_the_following_ones(bank):
    alice = bank.open_client("alice")
    bob = bank.open_client("bob")
    with pytest.raises(InsufficientFundsException):
        bank.transfer.execute(alice.account, bob.account, Amount(10))

    assert bank.register_client.execute("carol", PASSWORD)
    assert bank.deposit.execute(alice.id, alice.account, Amount(50))
    assert bank.transfer.execute(alice.account, bob.account, Amount(10))
