from enum import Enum
from typing import List

from domain.commontypes.types import AccountID, Amount
from domain.transaction import Transaction


class AccountNature(Enum):
    CREDIT_ACCOUNT = 1
    DEBIT_ACCOUNT = 2


class LedgerAccount:
    def __init__(self, account_id: AccountID, name: str, account_nature: AccountNature, transactions: List[Transaction]):
        self.account_id = account_id
        self._name = name
        self._account_nature = account_nature
        self.transactions = transactions

    def get_balance(self) -> Amount:
        balance = 0.0
        if self._account_nature == AccountNature.CREDIT_ACCOUNT:
            for t in self.transactions:
                if t.d_acc == self.account_id:
                    balance -= t.value
                else:
                    balance += t.value
        else:
            for t in self.transactions:
                if t.c_acc == self.account_id:
                    balance -= t.value
                else:
                    balance += t.value
        return balance
