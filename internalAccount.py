class internalAccount:
    def __init__(self,login,password,balance):
        self.m_login = login
        self.m_password = password
        self.m_balance = balance

    def balance(self):
        return self.m_balance

    def transfer(self,account,value):
        if self.m_balance < value:
            raise insufficientFundsException(self.m_balance, value)

        else:
            self.m_balance -= value
            account.incrementBalance(value)


class insufficientFundsException(Exception):
    def __init__(self,balance,value):
        self.balance = balance
        self.value = value
        super().__init__(f"{self.balance} is insufficient to get {self.value}")

