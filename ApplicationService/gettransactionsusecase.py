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


@dataclass
class TransactionData:
    debit_acc: int
    credit_acc: int
    value: float
    date: datetime

    def __str__(self):
        elemen_1 = self.date
        elemen_2 = self.debit_acc
        elemen_3 = self.credit_acc
        elemen_4 = self.value
        return f"{elemen_1} | {elemen_2} | {elemen_3} | {elemen_4}"


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
            t_debit = t.d_acc
            t_credit = t.c_acc
            t_value = t.value
            t_date = t.date

            t_data = TransactionData(t_debit, t_credit, t_value, t_date)

            acc_transactions_data.append(t_data)

        return acc_transactions_data
