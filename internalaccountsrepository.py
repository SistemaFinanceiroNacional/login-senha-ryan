import maybe
import internalAccount
from ApplicationService.connection_pool import connection_pool as cpool
from ApplicationService.identity import identity
import logging

logger = logging.getLogger("internalaccountsrepository")


class internalAccountsRepository:
    def __init__(self, connection_pool: cpool, identifier: identity):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add_account(self, new_login: str, new_password: str) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT * FROM accounts WHERE login = %s ", (new_login,))
        account_query_result = cursor.fetchone()

        if not account_query_result:
            cursor.execute("INSERT INTO accounts (login,password,balance) VALUES (%s,%s,%s)", (new_login, str(new_password), 0))

        return not account_query_result

    def authentication(self, login, password) -> maybe.maybe:
        logger.debug("Entered on authentication.")
        cursor = self.connection_pool.get_cursor(self.identifier)
        logger.debug("Got cursor.")
        cursor.execute("SELECT login, password, balance FROM accounts WHERE login=%s AND password=%s", (login, str(password)))
        logger.debug("Cursor execute ran.")
        find_login_list = cursor.fetchone()
        if find_login_list is not None:
            logger.debug("Account found.")
            return maybe.just(internalAccount.internalAccount(find_login_list[0], find_login_list[1], find_login_list[2]))
        logger.debug("Account not found.")
        return maybe.nothing()

    def update_balance(self, login: str, new_balance: float) -> None:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("UPDATE accounts SET balance=%s WHERE login=%s", (new_balance, login))