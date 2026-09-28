import math
from typing import List
from domain.transaction import Transaction, create_transaction
from domain.commontypes.types import AccountID

Amount = float

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

    def deposit(self, value: Amount) -> None:
        if not is_valid_deposit(value):
            raise InvalidValueToDeposit(value)
        transaction = create_transaction(
            BANK_DEPOSITS_ACCOUNT_ID, self._id, value
        )
        self._transactions.insert(0, transaction)

    def get_id(self) -> AccountID:
        return self._id

    def get_transactions(self) -> List[Transaction]:
        return self._transactions


def is_valid_deposit(value: Amount) -> bool:
    return math.isfinite(value) and value > 0


class InsufficientFundsException(Exception):
    def __init__(self, balance: Amount, value: Amount):
        super().__init__(f"{balance} is insufficient to get {value}")


class InvalidValueToTransfer(Exception):
    def __init__(self, value: Amount):
        super().__init__(f"{value} is a non-positive value to transfer.")


class InvalidValueToDeposit(Exception):
    def __init__(self, value: Amount):
        super().__init__(f"{value} is not a valid value to deposit.")
