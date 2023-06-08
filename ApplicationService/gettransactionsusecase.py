from dataclasses import dataclass
from datetime import datetime
from typing import List

from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountID,
    AccountsRepositoryInterface as a_repo
)
from ApplicationService.repositories.transactioncontextinterface import (
    TransactionContextInterface as cntx
)
from Domain.transaction import Transaction


@dataclass
class TransactionData:
    debit_acc: int
    credit_acc: int
    value: float
    date: datetime

    def __init__(self, transaction: Transaction):
        self.debit_acc = transaction.d_acc
        self.credit_acc = transaction.c_acc
        self.value = transaction.value
        self.date = transaction.date

    def __str__(self):
        date = self.date
        debit_acc = self.debit_acc
        credit_acc = self.credit_acc
        value = self.value
        return f"{date} | {debit_acc} | {credit_acc} | {value}"


class GetTransactionsUseCase:
    def __init__(self, acc_repository: a_repo, db_context: cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, acc_id: AccountID) -> List[TransactionData]:
        with self._db_context:
            acc = self._acc_repository.get_by_id(acc_id)
            acc_transactions = acc.get_transactions()
        acc_transactions_data = []
        for t in acc_transactions:
            t_data = TransactionData(t)
            acc_transactions_data.append(t_data)
        return acc_transactions_data
