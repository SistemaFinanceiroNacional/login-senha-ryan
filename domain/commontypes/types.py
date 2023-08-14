from uuid import UUID


ClientId = int
AccountId = UUID
Amount = float


class LedgerId:
    def __init__(self, acc_id: AccountId, digits: int):
        self.acc_id = acc_id
        self.digits = digits
