import logging
from password import password as pw
from ApplicationService.account import Account
from ApplicationService.connection_pool import connection_pool as cpool
from ApplicationService.repositories.identityinterface import (
    identityInterface
)
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface
)


logger = logging.getLogger("internalAccountsRepository")
accountID = int


class accountsRepository(AccountsRepositoryInterface):
    def __init__(self, connection_pool: cpool, identifier: identityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add_account(self, new_login: str, new_password: pw) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        query = "SELECT * FROM clients WHERE login = %s;"
        cursor.execute(query, (new_login,))
        account_query_result = cursor.fetchone()

        if not account_query_result:
            columns = "(login,password)"
            statements = "VALUES (%s,%s)"
            return_t = "RETURNING id"
            query = f"INSERT INTO clients {columns} {statements} {return_t};"
            cursor.execute(query, (new_login, str(new_password)))

            client_id = cursor.fetchone()

            statements = "VALUES (default)"
            query = f"INSERT INTO accounts {statements} {return_t};"
            cursor.execute(query)
            account_id = cursor.fetchone()

            columns = "(client_id, account_id)"
            statements = "VALUES (%s,%s)"
            table = "clients_accounts"
            query = f"INSERT INTO {table} {columns} {statements};"
            cursor.execute(query, (client_id, account_id))

        return not account_query_result

    def exists(self, destiny_id: int) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        query = "SELECT * FROM accounts WHERE id=%s;"
        cursor.execute(query, (destiny_id,))
        return cursor.fetchone() is not None

    def get_account_id(self, client_login: str) -> accountID:
        cursor = self.connection_pool.get_cursor(self.identifier)

        query = "SELECT id FROM clients WHERE login=%s;"
        cursor.execute(query, (client_login,))
        client_id = cursor.fetchone()[0]
        query = "SELECT account_id FROM clients_accounts WHERE client_id=%s;"
        cursor.execute(query, (client_id,))
        account_id = cursor.fetchone()[0]
        return account_id

    def update(self, acc: Account) -> None:
        cursor = self.connection_pool.get_cursor(self.identifier)
        transactions = acc.get_transactions()

        table = "transactions"
        columns = "(uuid, debit_account, credit_account, value, date)"
        statements = "VALUES (%s, %s, %s, %s, %s)"
        conflict = "ON CONFLICT (uuid) DO NOTHING"
        query = f"INSERT INTO {table} {columns} {statements} {conflict};"

        for t in transactions:
            data = t.get_transaction_data()
            cursor.execute(query, data)
