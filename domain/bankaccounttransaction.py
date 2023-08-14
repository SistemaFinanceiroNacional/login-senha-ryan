from uuid import UUID, uuid4
from datetime import datetime

from domain.commontypes.types import AccountId

RawBankTransaction = tuple[UUID, AccountId, AccountId, float, datetime]


class BankAccountTransaction:
    def __init__(self,
                 identifier: UUID,
                 debit_acc: AccountId,
                 credit_acc: AccountId,
                 value: float,
                 date: datetime
                 ):
        self.id = identifier
        self.d_acc = debit_acc
        self.c_acc = credit_acc
        self.value = value
        self.date = date

    def get_transaction_data(self) -> RawBankTransaction:
        return self.id, self.d_acc, self.c_acc, self.value, self.date


def create_transaction(
        d_acc: AccountId,
        c_acc: AccountId,
        value: float
) -> BankAccountTransaction:
    date = datetime.now()
    identifier = uuid4()
    transaction = BankAccountTransaction(identifier, d_acc, c_acc, value, date)
    return transaction


def create_transaction_from_raw(raw_transactions: RawBankTransaction):
    t_id, d_acc, c_acc, v, d = raw_transactions
    return BankAccountTransaction(t_id, d_acc, c_acc, v, d)
