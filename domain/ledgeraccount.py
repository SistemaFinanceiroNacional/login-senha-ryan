from enum import Enum
from typing import List

from domain.commontypes.types import Amount, LedgerId
from domain.ledgertransaction import LedgerTransaction


class AccountNature(Enum):
    CREDIT_ACCOUNT = 1
    DEBIT_ACCOUNT = 2


class LedgerAccount:
    def __init__(
            self,
            ledger_id: LedgerId,
            account_nature: AccountNature,
            transactions: List[LedgerTransaction]
    ):
        self.account_id = ledger_id
        self._account_nature = account_nature
        self.transactions = transactions

    def get_balance(self) -> Amount:
        balance = 0.0
        for t in self.transactions:
            def is_credit(acc_nature: AccountNature) -> bool:
                return acc_nature == AccountNature.CREDIT_ACCOUNT
            if is_credit(self._account_nature) and t.from_acc == self.account_id:
                balance -= t.value
            else:
                balance += t.value
        return balance

    def get_transactions(self) -> List[LedgerTransaction]:
        return self.transactions

    def add_transaction(self, transaction: LedgerTransaction):
        self.transactions.insert(0, transaction)
