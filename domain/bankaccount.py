from typing import List
from domain.transaction import Transaction, create_transaction
from domain.commontypes.types import AccountID

Amount = float


class BankAccount:
    def __init__(self,
                 account_id: AccountID,
                 transactions: List[Transaction]
                 ):
        self._id = account_id
        self._transactions = transactions

    def get_balance(self) -> Amount:
        balance = 0.0
        for t in self._transactions:
            if t.d_acc == self._id:
                balance -= t.value
            else:
                balance += t.value
        return balance

    def transfer(self, destiny_id: AccountID, value: Amount) -> None:
        if value <= 0:
            raise InvalidValueToTransfer(value)

        balance = self.get_balance()
        if balance < value:
            raise InsufficientFundsException(balance, value)
        else:
            transaction = create_transaction(self._id, destiny_id, value)
            self._transactions.insert(0, transaction)

    def get_id(self) -> AccountID:
        return self._id

    def get_transactions(self) -> List[Transaction]:
        return self._transactions


class InsufficientFundsException(Exception):
    def __init__(self, balance: Amount, value: Amount):
        super().__init__(f"{balance} is insufficient to get {value}")


class InvalidValueToTransfer(Exception):
    def __init__(self, value: Amount):
        super().__init__(f"{value} is a non-positive value to transfer.")
