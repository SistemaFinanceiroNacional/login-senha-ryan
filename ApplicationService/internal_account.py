from typing import List
from ApplicationService.transaction import Transaction, create_transaction
from password import password as pw


class internalAccount:
    def __init__(self,
                 login: str,
                 password: pw,
                 transactions: List[Transaction]
                 ):
        self._login = login
        self._password = password
        self._transactions = transactions

    def get_balance(self):
        balance = 0
        for t in self._transactions:
            if t.d_acc == self._login:
                balance -= t.value
            else:
                balance += t.value
        return balance

    def transfer(self, destiny_acc: str, value: float):
        if value <= 0:
            raise invalidValueToTransfer(value)

        balance = self.get_balance()
        if balance < value:
            raise insufficientFundsException(balance, value)
        else:
            transaction = create_transaction(self._login, destiny_acc, value)
            self._transactions.insert(0, transaction)

    def get_login(self):
        return self._login


class insufficientFundsException(Exception):
    def __init__(self, balance: float, value: float):
        self.balance = balance
        self.value = value
        super().__init__(f"{self.balance} is insufficient to get {self.value}")


class invalidValueToTransfer(Exception):
    def __init__(self, value: float):
        self.value = value
        super().__init__(f"{self.value} is a non-positive value to transfer.")
