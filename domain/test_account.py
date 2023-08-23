import uuid

from domain.bankaccount import (
    BankAccount,
    InsufficientFundsException
)
from domain.commontypes.types import LedgerType

from domain.ledgertransaction import create_ledger_transaction
from fake_config.fakes import ledger_debt_maker, ledger_cred_maker

BANK_ACCOUNT_1 = uuid.uuid4()
BANK_ACCOUNT_2 = uuid.uuid4()
BANK_DEFAULT_ID = uuid.uuid4()


def test_transfer1():
    debit_acc = BankAccount(
        BANK_ACCOUNT_1,
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_debt_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        0
    )

    debit_ledger_main = debit_acc._main_account
    bank_ledger_main = ledger_debt_maker(BANK_DEFAULT_ID, LedgerType.MAIN)
    t = create_ledger_transaction(
        bank_ledger_main.account_id,
        debit_ledger_main.account_id,
        20
    )
    debit_ledger_main.add_transaction(t)

    debit_acc.transfer(BANK_ACCOUNT_2, 10)
    assert debit_acc.get_balance() == 10


def test_transfer_poor_ryan():
    debit_acc = BankAccount(
        BANK_ACCOUNT_1,
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_debt_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        0
    )

    debit_ledger_main = debit_acc._main_account
    bank_ledger_main = ledger_debt_maker(BANK_DEFAULT_ID, LedgerType.MAIN)
    t = create_ledger_transaction(
        bank_ledger_main.account_id,
        debit_ledger_main.account_id,
        10
    )
    debit_ledger_main.add_transaction(t)

    try:
        debit_acc.transfer(BANK_ACCOUNT_2, 20)
        assert False
    except InsufficientFundsException:
        assert True


def test_transactions_static_size():
    debit_acc = BankAccount(
        BANK_ACCOUNT_1,
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_debt_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        0
    )

    debit_ledger_main = debit_acc._main_account
    bank_ledger_main = ledger_debt_maker(BANK_DEFAULT_ID, LedgerType.MAIN)
    t = create_ledger_transaction(
        bank_ledger_main.account_id,
        debit_ledger_main.account_id,
        10
    )
    debit_ledger_main.add_transaction(t)
    assert len(debit_ledger_main.get_transactions()) == 1


def test_transactions_incremented_size():
    debit_acc = BankAccount(
        BANK_ACCOUNT_1,
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_debt_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        0
    )

    debit_ledger_main = debit_acc._main_account
    bank_ledger_main = ledger_debt_maker(BANK_DEFAULT_ID, LedgerType.MAIN)
    t = create_ledger_transaction(
        bank_ledger_main.account_id,
        debit_ledger_main.account_id,
        10
    )
    debit_ledger_main.add_transaction(t)
    debit_acc.transfer(BANK_ACCOUNT_2, 10)
    assert len(debit_acc.get_transactions()) == 2


def test_no_balance():
    debit_acc = BankAccount(
        BANK_ACCOUNT_1,
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_debt_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        ledger_cred_maker(BANK_ACCOUNT_1, LedgerType.MAIN),
        0
    )

    debit_ledger_main = debit_acc._main_account
    bank_ledger_main = ledger_debt_maker(BANK_DEFAULT_ID, LedgerType.MAIN)
    t = create_ledger_transaction(
        bank_ledger_main.account_id,
        debit_ledger_main.account_id,
        10
    )
    debit_ledger_main.add_transaction(t)
    debit_acc.transfer(BANK_ACCOUNT_2, 10)
    assert debit_acc.get_balance() == 0
