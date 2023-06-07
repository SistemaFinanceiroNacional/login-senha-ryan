from typing import List
from Domain.transaction import Transaction, create_transaction


AccountID = int


class Account:
    def __init__(self,
                 account_id: int,
                 transactions: List[Transaction]
                 ):
        self._id = account_id
        self._transactions = transactions

    def get_balance(self) -> float:
        balance = 0
        for t in self._transactions:
            if t.d_acc == self._id:
                balance -= t.value
            else:
                balance += t.value
        return balance

    def transfer(self, destiny_id: int, value: float) -> None:
        if value <= 0:
            raise invalidValueToTransfer(value)

        balance = self.get_balance()
        if balance < value:
            raise insufficientFundsException(balance, value)
        else:
            transaction = create_transaction(self._id, destiny_id, value)
            self._transactions.insert(0, transaction)

    def get_id(self) -> AccountID:
        return self._id

    def get_transactions(self) -> List[Transaction]:
        return self._transactions


class insufficientFundsException(Exception):
    def __init__(self, balance: float, value: float):
        self.balance = balance
        self.value = value
        super().__init__(f"{self.balance} is insufficient to get {self.value}")


class invalidValueToTransfer(Exception):
    def __init__(self, value: float):
        self.value = value
        super().__init__(f"{self.value} is a non-positive value to transfer.")
