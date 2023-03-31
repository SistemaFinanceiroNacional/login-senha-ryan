from ApplicationService.externalAccount import externalAccount
from ApplicationService.repositories.internalaccountsrepository import internalAccountsRepository
from password import password as pw

class internalAccount:
    def __init__(self, login: str, password: pw, balance: float):
        self.m_login = login
        self.m_password = password
        self.m_balance = balance

    def balance(self):
        return self.m_balance

    def transfer(self, intoAccount: externalAccount, value: float):
        if value <= 0:
            raise invalidValueToTransfer(value)

        if self.m_balance < value:
            raise insufficientFundsException(self.m_balance, value)

        else:
            self.m_balance -= value
            intoAccount.incrementBalance(value)

    def login(self):
        return self.m_login

    def update(self, repository: internalAccountsRepository):
        repository.update_balance(self.m_login, self.m_balance)

class insufficientFundsException(Exception):
    def __init__(self, balance: float, value: float):
        self.balance = balance
        self.value = value
        super().__init__(f"{self.balance} is insufficient to get {self.value}")

class invalidValueToTransfer(Exception):
    def __init__(self, value: float):
        self.value = value
        super().__init__(f"{self.value} is a non-positive value to transfer.")