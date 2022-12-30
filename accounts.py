import maybe
import internalAccount

class accounts:
    def __init__(self,archiveCursor):
        self.archive = archiveCursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_account(self, new_login, new_password):
        self.archive.execute("SELECT * FROM accounts WHERE login = %s ", (new_login,))
        x = self.archive.fetchone()

        if not x:
            self.archive.execute("INSERT INTO accounts (login,password,balance) VALUES (%s,%s,%s)", (new_login, str(new_password), 0))

        return not x

    def authentication(self, login, password):
        self.archive.execute("SELECT login, password, balance FROM accounts WHERE login=%s AND password=%s", (login, str(password)))
        findLoginList = self.archive.fetchone()
        if findLoginList is not None:
            return maybe.just(internalAccount.internalAccount(findLoginList[0], findLoginList[1], findLoginList[2]))
        return maybe.nothing()

    def updateBalance(self, login, new_balance):
        self.archive.execute("UPDATE accounts SET balance=%s WHERE login=%s", (new_balance, login))
