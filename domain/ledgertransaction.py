from datetime import datetime
from uuid import UUID
from domain.commontypes.types import LedgerId


RawLedgerTransaction = tuple[UUID, LedgerId, LedgerId, float, datetime]


class LedgerTransaction:
    class BankAccountTransaction:
        def __init__(self,
                     identifier: UUID,
                     from_acc: LedgerId,
                     to_acc: LedgerId,
                     value: float,
                     date: datetime
                     ):
            self.id = identifier
            self.from_acc = from_acc
            self.to_acc = to_acc
            self.value = value
            self.date = date

        def get_transaction_data(self) -> RawLedgerTransaction:
            return self.id, self.from_acc, self.to_acc, self.value, self.date
