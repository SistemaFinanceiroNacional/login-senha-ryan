from enum import Enum
from typing import List

from domain.commontypes.types import AccountId, Amount
from domain.bankaccounttransaction import BankAccountTransaction


class AccountNature(Enum):
    CREDIT_ACCOUNT = 1
    DEBIT_ACCOUNT = 2


class LedgerAccount:
    def __init__(
            self,
            account_id: AccountId,
            name: str,
            account_nature: AccountNature,
            transactions: List[BankAccountTransaction]
    ):
        self.account_id = account_id
        self._name = name
        self._account_nature = account_nature
        self.transactions = transactions

    def get_balance(self) -> Amount:
        balance = 0.0
        for t in self.transactions:
            def is_credit(acc_nature: AccountNature) -> bool:
                return acc_nature == AccountNature.CREDIT_ACCOUNT
            if is_credit(self._account_nature) and t.d_acc == self.account_id:
                balance -= t.value
            else:
                balance += t.value
        return balance

    def get_transactions(self) -> List[BankAccountTransaction]:
        return self.transactions

    def add_transaction(self, transaction: BankAccountTransaction):
        self.transactions.insert(0, transaction)
