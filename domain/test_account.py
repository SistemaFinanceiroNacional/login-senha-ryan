import uuid

from domain.bankaccount import (
    BankAccount,
    InsufficientFundsException
)
from domain.bankaccounttransaction import create_transaction
from domain.commontypes.types import LedgerId, LedgerType
from domain.ledgeraccount import LedgerAccount, AccountNature
from domain.ledgertransaction import create_ledger_transaction


DEBIT_ID = uuid.uuid4()
CREDIT_ID = uuid.uuid4()
BANK_DEFAULT_ID = uuid.uuid4()

def ledger_debt_maker(ledger_type: LedgerType):
    ledger_id = LedgerId(DEBIT_ID, ledger_type)
    return LedgerAccount(ledger_id, AccountNature.DEBIT_ACCOUNT, [])

def ledger_cred_maker(ledger_type: LedgerType):
    ledger_id = LedgerId(CREDIT_ID, ledger_type)
    return LedgerAccount(ledger_id, AccountNature.CREDIT_ACCOUNT, [])

def ledger_bank_maker(ledger_type: LedgerType):
    ledger_id = LedgerId(BANK_DEFAULT_ID, ledger_type)
    return LedgerAccount(ledger_id, AccountNature.DEBIT_ACCOUNT, [])

def test_transfer1():
    debit_acc = BankAccount(
        DEBIT_ID,
        ledger_debt_maker(LedgerType.MAIN),
        ledger_debt_maker(LedgerType.DRAFT),
        ledger_debt_maker(LedgerType.STAGE),
        0
    )
    credit_acc = BankAccount(
        CREDIT_ID,
        ledger_cred_maker(LedgerType.MAIN),
        ledger_cred_maker(LedgerType.DRAFT),
        ledger_cred_maker(LedgerType.STAGE),
        0
    )

    debit_ledger_main = debit_acc._main_account
    bank_ledger_main = ledger_bank_maker(LedgerType.MAIN)
    t = create_ledger_transaction(
        bank_ledger_main.account_id,
        debit_ledger_main.account_id,
        20
    )
    debit_ledger_main.add_transaction(t)

    debit_acc.transfer(CREDIT_ID, 10)
    assert debit_acc.get_balance() == 10


def test_transfer_poor_ryan():
    t = create_transaction(1, 2, 10)
    x = BankAccount(2, [t])
    y = 3
    try:
        x.transfer(y, 20)
        assert False
    except InsufficientFundsException:
        assert True


def test_transactions_static_size():
    t = create_transaction(1, 2, 10)
    x = BankAccount(2, [t])
    assert len(x._transactions) == 1


def test_transactions_incremented_size():
    t = create_transaction(1, 2, 10)
    x = BankAccount(2, [t])
    y = 3
    x.transfer(y, 10)
    assert len(x._transactions) == 2


def test_no_balance():
    t = create_transaction(1, 2, 10)
    x = BankAccount(2, [t])
    y = 3
    x.transfer(y, 10)
    assert x.get_balance() == 0
