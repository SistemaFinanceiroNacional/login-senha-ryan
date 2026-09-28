import pytest

from domain.amount import Amount


def reload_account(bank, account_id):
    with bank.context:
        maybe_account = bank.accounts.get_by_id(account_id)
    return maybe_account.or_else_throw(AssertionError("account vanished"))


def save(bank, account) -> None:
    with bank.context:
        bank.accounts.update(account)


@pytest.mark.integration
def test_update_persists_new_transactions(bank):
    alice = bank.open_client("alice")
    account = reload_account(bank, alice.account)

    account.deposit(Amount(10))
    save(bank, account)

    reloaded = reload_account(bank, alice.account)
    assert [t.value for t in reloaded.get_transactions()] == [Amount(10)]


@pytest.mark.integration
def test_update_does_not_duplicate_existing_transactions(bank):
    alice = bank.open_client("alice")
    account = reload_account(bank, alice.account)
    account.deposit(Amount(10))
    save(bank, account)

    save(bank, reload_account(bank, alice.account))

    reloaded = reload_account(bank, alice.account)
    assert len(reloaded.get_transactions()) == 1


@pytest.mark.integration
@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="transactions.value is a FLOAT column (issue #116)")
def test_large_amounts_are_persisted_exactly(bank):
    alice = bank.open_client("alice")
    large = Amount("1234567890123456.78")
    assert bank.deposit.execute(alice.id, alice.account, large)

    reloaded = reload_account(bank, alice.account)

    assert [t.value for t in reloaded.get_transactions()] == [large]
