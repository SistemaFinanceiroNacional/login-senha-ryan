from uuid import UUID, uuid4
from datetime import datetime

from domain.amount import Amount


class Transaction:
    def __init__(self,
                 identifier: UUID,
                 debit_acc: int,
                 credit_acc: int,
                 value: Amount,
                 date: datetime
                 ):
        self.id = identifier
        self.d_acc = debit_acc
        self.c_acc = credit_acc
        self.value = value
        self.date = date


def create_transaction(d_acc: int, c_acc: int, value: Amount) -> Transaction:
    date = datetime.now()
    identifier = uuid4()
    transaction = Transaction(identifier, d_acc, c_acc, value, date)
    return transaction
