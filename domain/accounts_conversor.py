from domain.bankaccount import BankAccount
from domain.ledgeraccount import LedgerAccount


def get_stage_account(bank_acc: BankAccount) -> LedgerAccount:
    return bank_acc.stage_account
