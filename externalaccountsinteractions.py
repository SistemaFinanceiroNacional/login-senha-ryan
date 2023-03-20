import externalAccount
import maybe

class externalAccountsInteractions:
    def __init__(self, connection_pool, identifier):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def get_by_login(self, login):
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT login FROM accounts WHERE login=%s", (login,))
        possibleLogin = cursor.fetchone()
        if possibleLogin is not None:
            return maybe.just(externalAccount.externalAccount(possibleLogin[0]))

        else:
            return maybe.nothing()

    def update(self, login, incrementBalance):
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("UPDATE accounts SET balance=balance+%s WHERE login=%s", (incrementBalance, login))
