from typing import List
from domain.amount import Amount
from domain.transaction import Transaction, create_transaction
from domain.commontypes.types import AccountID

Money = float

# Created by the first migration; money deposited in the bank is debited
# from it.
BANK_DEPOSITS_ACCOUNT_ID: AccountID = 1


class BankAccount:
    def __init__(self,
                 account_id: AccountID,
                 transactions: List[Transaction]
                 ):
        self._id = account_id
        self._transactions = transactions

    def get_balance(self) -> Money:
        balance = 0.0
        for t in self._transactions:
            if t.d_acc == self._id:
                balance -= t.value
            else:
                balance += t.value
        return balance

    def transfer(self, destiny_id: AccountID, value: Money) -> None:
        if value <= 0:
            raise InvalidValueToTransfer(value)

        balance = self.get_balance()
        if balance < value:
            raise InsufficientFundsException(balance, value)
        else:
            transaction = create_transaction(self._id, destiny_id, value)
            self._transactions.insert(0, transaction)

    def deposit(self, amount: Amount) -> None:
        transaction = create_transaction(
            BANK_DEPOSITS_ACCOUNT_ID, self._id, amount.to_float()
        )
        self._transactions.insert(0, transaction)

    def get_id(self) -> AccountID:
        return self._id

    def get_transactions(self) -> List[Transaction]:
        return self._transactions


class InsufficientFundsException(Exception):
    def __init__(self, balance: Money, value: Money):
        super().__init__(f"{balance} is insufficient to get {value}")


class InvalidValueToTransfer(Exception):
    def __init__(self, value: Money):
        super().__init__(f"{value} is a non-positive value to transfer.")
