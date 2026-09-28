from typing import List
from domain.amount import Amount
from domain.money import Money
from domain.transaction import Transaction, create_transaction
from domain.commontypes.types import AccountID

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
        balance = Money.zero()
        for t in self._transactions:
            if t.d_acc == self._id:
                balance -= t.value
            else:
                balance += t.value
        return balance

    def transfer(self, destiny_id: AccountID, amount: Amount) -> None:
        balance = self.get_balance()
        if balance < amount:
            raise InsufficientFundsException(balance, amount)
        else:
            transaction = create_transaction(self._id, destiny_id, amount)
            self._transactions.insert(0, transaction)

    def deposit(self, amount: Amount) -> None:
        transaction = create_transaction(
            BANK_DEPOSITS_ACCOUNT_ID, self._id, amount
        )
        self._transactions.insert(0, transaction)

    def get_id(self) -> AccountID:
        return self._id

    def get_transactions(self) -> List[Transaction]:
        return self._transactions


class InsufficientFundsException(Exception):
    def __init__(self, balance: Money, amount: Amount):
        super().__init__(f"{balance} is insufficient to get {amount}")
