import maybe
import account
import condition

class contas():
    def __init__(self,archiveCursor):
        self.archive = archiveCursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_account(self,new_login,new_password):
        x = self.archive.execute("SELECT * FROM account WHERE login=%s",(new_login,))

        if not x:
            self.archive.execute("INSERT INTO account (login,password,balance) VALUES (%s,%s,%s)", (new_login,new_password,0))

        return not x

    def authentication(self,login,password):
        self.archive.execute("SELECT * FROM account WHERE login=%s AND password=%s", (login, str(password)))
        findLoginList = self.archive.fetchone()
        if findLoginList is not None:
            return maybe.just(account.account(findLoginList[1],findLoginList[2],findLoginList[3]))
        return maybe.nothing()