from dataclasses import dataclass
from datetime import datetime
from typing import List

from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as AccRepo
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)
from domain.bankaccount import BankAccount
from domain.bankaccounttransaction import BankAccountTransaction
from domain.commontypes.types import AccountId
from maybe import Maybe


@dataclass
class TransactionData:
    debit_acc: int
    credit_acc: int
    value: float
    date: datetime

    def __init__(self, transaction: BankAccountTransaction):
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
    def __init__(self, acc_repository: AccRepo, db_context: Cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, acc_id: AccountId) -> Maybe[List[TransactionData]]:
        with self._db_context:
            maybe_acc = self._acc_repository.get_by_id(acc_id)

        def transactions_data(acc: BankAccount) -> List[TransactionData]:
            transactions = acc.get_transactions()
            return self._get_transactions_data(transactions)

        acc_transactions = maybe_acc.map(transactions_data)
        return acc_transactions

    def _get_transactions_data(self, transactions) -> List[TransactionData]:
        transactions_data = []
        for t in transactions:
            t_data = TransactionData(t)
            transactions_data.append(t_data)
        return transactions_data
