from uuid import UUID, uuid4
from datetime import datetime


class Transaction:
    def __init__(self,
                 debit_acc: str,
                 credit_acc: str,
                 value: float,
                 date: datetime,
                 identifier: UUID
                 ):
        self.d_acc = debit_acc
        self.c_acc = credit_acc
        self.value = value
        self.date = date
        self.id = identifier


def create_transaction(d_acc: str, c_acc: str, value: float) -> Transaction:
    date = datetime.now()
    identifier = uuid4()
    transaction = Transaction(d_acc, c_acc, value, date, identifier)
    return transaction
