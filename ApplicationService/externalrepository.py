import maybe
from ApplicationService.external_account import externalAccount
from ApplicationService.connection_pool import connection_pool
from ApplicationService.threadIdentity import identity
from ApplicationService.repositories.externalaccountsrepository import externalAccountsRepository

class externalRepository(externalAccountsRepository):
    def __init__(self, cpool: connection_pool, identifier: identity):
        self.connection_pool = cpool
        self.identifier = identifier

    def get_by_login(self, login: str) -> maybe.maybe[externalAccount]:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT _login FROM accounts WHERE _login=%s", (login,))
        possibleLogin = cursor.fetchone()
        if possibleLogin is not None:
            return maybe.just(externalAccount(possibleLogin[0]))

        else:
            return maybe.nothing()

    def update(self, extAccount: externalAccount) -> None:
        incrementBalance = extAccount.get_increment_balance()
        login = extAccount.get_login()

        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("UPDATE accounts SET balance=balance+%s WHERE _login=%s", (incrementBalance, login))
