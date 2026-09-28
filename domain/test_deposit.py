import math

import pytest

from domain.bankaccount import (
    BANK_DEPOSITS_ACCOUNT_ID,
    BankAccount,
    InvalidValueToDeposit
)

NOT_IMPLEMENTED = "deposit not implemented yet (issue #110)"


@pytest.mark.xfail(strict=True, reason=NOT_IMPLEMENTED,
                   raises=NotImplementedError)
def test_deposit_increases_balance():
    account = BankAccount(2, [])

    account.deposit(150.5)
    account.deposit(49.5)

    assert account.get_balance() == 200.0


@pytest.mark.xfail(strict=True, reason=NOT_IMPLEMENTED,
                   raises=NotImplementedError)
def test_deposit_is_money_coming_from_the_bank_deposits_account():
    account = BankAccount(2, [])

    account.deposit(150.5)

    [transaction] = account.get_transactions()
    assert transaction.d_acc == BANK_DEPOSITS_ACCOUNT_ID
    assert transaction.c_acc == 2
    assert transaction.value == 150.5


@pytest.mark.xfail(strict=True, reason=NOT_IMPLEMENTED,
                   raises=NotImplementedError)
@pytest.mark.parametrize("value", [0, -10, math.nan, math.inf])
def test_deposit_rejects_invalid_values(value):
    account = BankAccount(2, [])

    with pytest.raises(InvalidValueToDeposit):
        account.deposit(value)

    assert account.get_transactions() == []
