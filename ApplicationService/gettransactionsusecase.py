from dataclasses import dataclass
from datetime import datetime
from typing import List

from Infrastructure.accountsrepository import (
    AccountsRepositoryInterface as iar,
    AccountID
)
from ApplicationService.repositories.transactioncontext import (
    transactioncontext as cntx
)

@dataclass
class TransactionData:
    debit_acc: int
    credit_acc: int
    value: float
    date: datetime

    def __str__(self):
        return f"{self.date} | {self.debit_acc} | {self.credit_acc} | {self.value}"


class GetTransactionsUseCase:
    def __init__(self, acc_repository: iar, db_context: cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, acc_id: AccountID) -> List[TransactionData]:
        with self._db_context:
            acc = self._acc_repository.get_by_id(acc_id)
            acc_transactions = acc.get_transactions()

        acc_transactions_data = []
        for t in acc_transactions:
            t_debit = t.d_acc
            t_credit = t.c_acc
            t_value = t.value
            t_date = t.date

            t_data = TransactionData(t_debit, t_credit, t_value, t_date)

            acc_transactions_data.append(t_data)

        return acc_transactions_data
