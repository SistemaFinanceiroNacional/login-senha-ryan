from datetime import datetime
from uuid import UUID, uuid4
from domain.commontypes.types import LedgerId, Amount

RawLedgerTransaction = tuple[UUID, LedgerId, LedgerId, float, datetime]


class LedgerTransaction:
    def __init__(self,
                 identifier: UUID,
                 from_acc: LedgerId,
                 to_acc: LedgerId,
                 value: Amount,
                 date: datetime
                 ):
        self.id = identifier
        self.from_acc = from_acc
        self.to_acc = to_acc
        self.value = value
        self.date = date

    def get_transaction_data(self) -> RawLedgerTransaction:
        return self.id, self.from_acc, self.to_acc, self.value, self.date


def create_ledger_transaction(
        origin_id: LedgerId,
        destiny_id: LedgerId,
        value: Amount,
):
    date = datetime.now()
    identifier = uuid4()
    return LedgerTransaction(identifier, origin_id, destiny_id, value, date)
