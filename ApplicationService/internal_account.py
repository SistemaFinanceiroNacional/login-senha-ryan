from ApplicationService.external_account import externalAccount
from password import password as pw

class internalAccount:
    def __init__(self, login: str, password: pw, balance: float):
        self._login = login
        self._password = password
        self._balance = balance

    def get_balance(self):
        return self._balance

    def transfer(self, intoAccount: externalAccount, value: float):
        if value <= 0:
            raise invalidValueToTransfer(value)

        if self._balance < value:
            raise insufficientFundsException(self._balance, value)

        else:
            self._balance -= value
            intoAccount.increment_balance(value)

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