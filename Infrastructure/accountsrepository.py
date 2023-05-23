import logging
from typing import Iterable, List

from password import Password as pw
from Domain.account import Account
from Domain.transaction import Transaction, create_transaction_from_raw
from Infrastructure.connection_pool import (
    connection_pool as cpool,
    cursor as c
)
from ApplicationService.repositories.identityinterface import (
    identityInterface
)
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface
)

logger = logging.getLogger("internalAccountsRepository")
AccountID = int
ClientID = int
Transactions = List[Transaction]


class AccountsRepository(AccountsRepositoryInterface):
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

    def get_by_client_id(self, client_id: ClientID) -> Iterable[AccountID]:
        cursor = self.connection_pool.get_cursor(self.identifier)

        query = "SELECT account_id FROM clients_accounts WHERE client_id=%s;"
        cursor.execute(query, (client_id,))
        accounts_ids_tuples = cursor.fetchall()
        accounts_ids = map(lambda item: item[0], accounts_ids_tuples)
        return accounts_ids

    def get_balance(self, account_id: AccountID):
        cursor = self.connection_pool.get_cursor(self.identifier)

        transactions = self._get_transactions(account_id, cursor)
        acc = Account(account_id, transactions)
        return acc.get_balance()

    def _get_transactions(self, account_id: int, cursor: c) -> Transactions:
        table = "transactions t"
        columns = "t.*"
        condition = "t.debit_account = a.id OR t.credit_account = a.id"
        where = "a.id = %s"
        query = f"SELECT {columns} " \
                f"FROM {table} " \
                f"JOIN accounts a ON {condition} " \
                f"WHERE {where};"
        cursor.execute(query, (account_id,))
        raw_transactions = cursor.fetchall()
        transactions = []
        for t in raw_transactions:
            new_t = create_transaction_from_raw(t)
            transactions.append(new_t)
        return transactions
