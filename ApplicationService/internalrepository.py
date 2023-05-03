from maybe import maybe, just, nothing
from password import password as pw
from ApplicationService.internal_account import internalAccount as ia
from ApplicationService.connection_pool import connection_pool as cpool
from ApplicationService.threadIdentity import identity
from ApplicationService.repositories.internalaccountsrepository import (
    internalAccountsRepository
)
import logging

logger = logging.getLogger("internalAccountsRepository")


class internalRepository(internalAccountsRepository):
    def __init__(self, connection_pool: cpool, identifier: identity):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add_account(self, new_login: str, new_password: pw) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        query = "SELECT * FROM accounts WHERE login = %s"
        cursor.execute(query, (new_login,))
        account_query_result = cursor.fetchone()

        if not account_query_result:
            columns = "(login,password,balance)"
            values_statements = "VALUES (%s,%s,%s)"
            query = f"INSERT INTO accounts {columns} {values_statements}"
            cursor.execute(query, (new_login, str(new_password), 0))

        return not account_query_result

    def authentication(self, login: str, password: pw) -> maybe[ia]:
        cursor = self.connection_pool.get_cursor(self.identifier)
        select = "login, password, balance"
        table = "accounts"
        conditions = "login=%s AND password=%s"
        query = f"SELECT {select} FROM {table} WHERE {conditions}"
        cursor.execute(query, (login, str(password)))
        find_login_list = cursor.fetchone()

        if find_login_list is not None:
            user_login = find_login_list[0]
            user_password = find_login_list[1]
            user_balance = find_login_list[2]
            return just(ia(user_login, user_password, user_balance))

        return nothing()

    def update_balance(self, intAccount: ia) -> None:
        login = intAccount.get_login()
        new_balance = intAccount.get_balance()

        cursor = self.connection_pool.get_cursor(self.identifier)
        query = "UPDATE accounts SET balance=%s WHERE login=%s"
        cursor.execute(query, (new_balance, login))
