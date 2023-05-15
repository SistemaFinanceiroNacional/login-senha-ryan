from typing import List
import logging
from maybe import maybe, just, nothing
from password import password as pw
from ApplicationService.account import Account
from ApplicationService.connection_pool import connection_pool as cpool
from ApplicationService.threadIdentity import identity
from ApplicationService.repositories.internalaccountsrepository import (
    internalAccountsRepository
)
from ApplicationService.transaction import (
    Transaction,
    create_transaction_from_raw
)
from ApplicationService.client import Client
from ApplicationService.repositories.connectionInterface import cursor as c

logger = logging.getLogger("internalAccountsRepository")


class accountsRepository(internalAccountsRepository):
    def __init__(self, connection_pool: cpool, identifier: identity):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add_account(self, new_login: str, new_password: pw) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        query = "SELECT * FROM clients WHERE login = %s"
        cursor.execute(query, (new_login,))
        account_query_result = cursor.fetchone()

        if not account_query_result:
            columns = "(login,password)"
            statements = "VALUES (%s,%s)"
            return_t = "RETURNING id"
            query = f"INSERT INTO clients {columns} {statements} {return_t}"
            cursor.execute(query, (new_login, str(new_password)))

            client_id = cursor.fetchone()

            statements = "VALUES (default)"
            query = f"INSERT INTO accounts {statements} {return_t}"
            cursor.execute(query)
            account_id = cursor.fetchone()

            columns = "(client_id, account_id)"
            statements = "VALUES (%s,%s)"
            table = "clients_accounts"
            query = f"INSERT INTO {table} {columns} {statements}"
            cursor.execute(query, (client_id, account_id))

        return not account_query_result

    def authentication(self, login: str, password: pw) -> maybe[Client]:
        cursor = self.connection_pool.get_cursor(self.identifier)
        select = "id, login, password"
        table = "clients"
        conditions = "login=%s AND password=%s"
        query = f"SELECT {select} FROM {table} WHERE {conditions}"
        cursor.execute(query, (login, str(password)))
        find_login_list = cursor.fetchone()

        if find_login_list is not None:
            client_id = find_login_list[0]
            user_login = find_login_list[1]
            user_password = find_login_list[2]
            user_accounts = self.get_user_accounts(client_id, cursor)
            return just(Client(user_login, user_password, user_accounts))

        return nothing()

    def exists(self, login: str) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        query = "SELECT * FROM clients WHERE login=%s"
        cursor.execute(query, (login,))
        return cursor.fetchone() is not None

    def get_user_accounts(self, client_id: int, cursor: c) -> List[Account]:
        table = "clients_accounts"
        statements = "account_id"
        query = f"SELECT {statements} " \
                f"FROM {table} " \
                f"WHERE client_id=%s"
        cursor.execute(query, (client_id,))
        accounts_data = cursor.fetchall()
        accounts = []
        for data in accounts_data:
            acc_id = data[0]
            transactions = self.get_transactions(acc_id, cursor)
            acc = Account(acc_id, transactions)
            accounts.append(acc)
        return accounts

    def get_transactions(self, account_id: int, cursor: c) -> List[Transaction]:
        table = "transactions t"
        columns = "t.*"
        condition = "t.debit_account = a.id OR t.credit_account = a.id"
        where = "a.id = %s"
        query = f"SELECT {columns} " \
                f"FROM {table} " \
                f"JOIN accounts a ON {condition} " \
                f"WHERE {where}"
        cursor.execute(query, (account_id,))
        raw_transactions = cursor.fetchall()
        transactions = []
        for t in raw_transactions:
            new_t = create_transaction_from_raw(t)
            transactions.append(new_t)
        return transactions

    def get_account_id(self, client_login: str):
        cursor = self.connection_pool.get_cursor(self.identifier)

        query = "SELECT id FROM clients WHERE login=%s"
        cursor.execute(query, (client_login,))
        client_id = cursor.fetchone()[0]
        query = "SELECT account_id FROM clients_accounts WHERE client_id=%s"
        cursor.execute(query, (client_id,))
        account_id = cursor.fetchone()[0]
        return account_id
