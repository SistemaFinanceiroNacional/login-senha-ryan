from ApplicationService.externalAccount import externalAccount
import maybe
from ApplicationService.connection_pool import connection_pool
from ApplicationService.identity import identity
from ApplicationService.repositories.externalaccountsrepository import externalAccountsRepository

class externalRepository(externalAccountsRepository):
    def __init__(self, cpool: connection_pool, identifier: identity):
        self.connection_pool = cpool
        self.identifier = identifier

    def get_by_login(self, login: str) -> maybe.maybe:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT login FROM accounts WHERE login=%s", (login,))
        possibleLogin = cursor.fetchone()
        if possibleLogin is not None:
            return maybe.just(externalAccount(possibleLogin[0]))

        else:
            return maybe.nothing()

    def update(self, login: str, incrementBalance: float):
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("UPDATE accounts SET balance=balance+%s WHERE login=%s", (incrementBalance, login))
