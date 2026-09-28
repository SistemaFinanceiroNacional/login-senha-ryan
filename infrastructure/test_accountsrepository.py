import pytest


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

    account.deposit(10.0)
    save(bank, account)

    reloaded = reload_account(bank, alice.account)
    assert [t.value for t in reloaded.get_transactions()] == [10.0]


@pytest.mark.integration
def test_update_does_not_duplicate_existing_transactions(bank):
    alice = bank.open_client("alice")
    account = reload_account(bank, alice.account)
    account.deposit(10.0)
    save(bank, account)

    save(bank, reload_account(bank, alice.account))

    reloaded = reload_account(bank, alice.account)
    assert len(reloaded.get_transactions()) == 1
