from uuid import UUID, uuid4
from datetime import datetime


RawTransaction = tuple[UUID, int, int, float, datetime]


class Transaction:
    def __init__(self,
                 identifier: UUID,
                 debit_acc: int,
                 credit_acc: int,
                 value: float,
                 date: datetime
                 ):
        self.id = identifier
        self.d_acc = debit_acc
        self.c_acc = credit_acc
        self.value = value
        self.date = date

    def get_transaction_data(self) -> RawTransaction:
        return self.id, self.d_acc, self.c_acc, self.value, self.date


def create_transaction(d_acc: int, c_acc: int, value: float) -> Transaction:
    date = datetime.now()
    identifier = uuid4()
    transaction = Transaction(identifier, d_acc, c_acc, value, date)
    return transaction


def create_transaction_from_raw(raw_transactions: RawTransaction):
    t_id, d_acc, c_acc, v, d = raw_transactions
    return Transaction(t_id, d_acc, c_acc, v, d)
