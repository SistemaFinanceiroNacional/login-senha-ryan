from maybe import maybe, just, nothing
from ApplicationService.internal_account import internalAccount
from password import password as pw
from ApplicationService.connection_pool import connection_pool as cpool
from ApplicationService.threadIdentity import identity
from ApplicationService.repositories.internalaccountsrepository import internalAccountsRepository
import logging

logger = logging.getLogger("internalAccountsRepository")

class internalRepository(internalAccountsRepository):
    def __init__(self, connection_pool: cpool, identifier: identity):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add_account(self, new_login: str, new_password: pw) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT * FROM accounts WHERE login = %s ", (new_login,))
        account_query_result = cursor.fetchone()

        if not account_query_result:
            cursor.execute("INSERT INTO accounts (login,password,balance) VALUES (%s,%s,%s)", (new_login, str(new_password), 0))

        return not account_query_result

    def authentication(self, login: str, password: pw) -> maybe[internalAccount]:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT login, password, balance FROM accounts WHERE login=%s AND password=%s", (login, str(password)))
        find_login_list = cursor.fetchone()

        if find_login_list is not None:
            return just(internalAccount(find_login_list[0], find_login_list[1], find_login_list[2]))

        return nothing()

    def update_balance(self, intAccount: internalAccount) -> None:
        login = intAccount.get_login()
        new_balance = intAccount.get_balance()

        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("UPDATE accounts SET balance=%s WHERE login=%s", (new_balance, login))