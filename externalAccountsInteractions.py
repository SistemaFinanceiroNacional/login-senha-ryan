import externalAccount
import maybe


class externalAccountsInteractions:
    def __init__(self, cursor):
        self.cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def getByLogin(self,login):
        self.cursor.execute("SELECT login FROM account WHERE login=%s",(login,))
        possibleLogin = self.cursor.fetchone()
        if possibleLogin is not None:
            return maybe.just(externalAccount.externalAccount(possibleLogin[0]))

        else:
            return maybe.nothing()