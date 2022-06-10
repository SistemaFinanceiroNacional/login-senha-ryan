class internalAccount:
    def __init__(self,login,password,balance):
        self.m_login = login
        self.m_password = password
        self.m_balance = balance

    def balance(self):
        return self.m_balance

    def transfer(self,intoAccount,value):
        if value <= 0:
            raise invalidValueToTransfer(value)

        if self.m_balance < value:
            raise insufficientFundsException(self.m_balance, value)

        else:
            self.m_balance -= value
            intoAccount.incrementBalance(value)

    def login(self):
        return self.m_login

    def update(self, repository):
        repository.updateBalance(self.m_login,self.m_balance)

class insufficientFundsException(Exception):
    def __init__(self,balance,value):
        self.balance = balance
        self.value = value
        super().__init__(f"{self.balance} is insufficient to get {self.value}")

class invalidValueToTransfer(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(f"{self.value} is a non-positive value to transfer.")