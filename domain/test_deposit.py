from domain.amount import Amount
from domain.bankaccount import BANK_DEPOSITS_ACCOUNT_ID, BankAccount
from domain.money import Money


def test_deposit_increases_balance():
    account = BankAccount(2, [])

    account.deposit(Amount("150.50"))
    account.deposit(Amount("49.50"))

    assert account.get_balance() == Money("200.00")


def test_deposit_is_money_coming_from_the_bank_deposits_account():
    account = BankAccount(2, [])

    account.deposit(Amount("150.50"))

    [transaction] = account.get_transactions()
    assert transaction.d_acc == BANK_DEPOSITS_ACCOUNT_ID
    assert transaction.c_acc == 2
    assert transaction.value == Amount("150.50")
