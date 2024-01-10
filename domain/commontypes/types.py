from enum import Enum
from uuid import UUID


ClientId = int
AccountId = UUID
Amount = float


class LedgerType(Enum):
    MAIN = 1
    DRAFT = 2
    STAGE = 3


class LedgerId:
    def __init__(self, acc_id: AccountId, digits: LedgerType):
        self.acc_id = acc_id
        self.digits = digits
