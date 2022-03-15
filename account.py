class account():
    def __init__(self,login,senha,saldo):
        self.m_login = login
        self.m_senha = senha
        self.m_saldo = saldo

    def saldo(self):
        return self.m_saldo