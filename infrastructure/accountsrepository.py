from typing import Iterable, List
from maybe import Maybe, Just, Nothing
from domain.transaction import Transaction, create_transaction_from_raw
from infrastructure.connection_pool import (
    ConnectionPool as CPool,
)
from infrastructure.identityinterface import (
    IdentityInterface
)
from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface,
    BankAccount,
    AccountID,
    ClientID
)

Transactions = List[Transaction]


class AccountsRepository(AccountsRepositoryInterface):
    def __init__(self, connection_pool: CPool, identifier: IdentityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add_account(self, client_id: ClientID):
        cursor = self.connection_pool.get_cursor(self.identifier)

        return_t = "RETURNING id"
        statements = "VALUES (default)"
        query = f"INSERT INTO accounts {statements} {return_t};"
        cursor.execute(query)
        fetchone = cursor.fetchone()
        if fetchone is None:
            raise Exception("WTF: ID must not be null after an insertion.")
        account_id = fetchone[0]

        columns = "(client_id, account_id)"
        statements = "VALUES (%s,%s)"
        table = "clients_accounts"
        query = f"INSERT INTO {table} {columns} {statements};"
        cursor.execute(query, (client_id, account_id))

    def exists(self, destiny_id: int) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        query = "SELECT * FROM accounts WHERE id=%s;"
        cursor.execute(query, (destiny_id,))
        return cursor.fetchone() is not None

    def update(self, acc: BankAccount):
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

    def get_by_id(self, account_id: AccountID) -> Maybe[BankAccount]:
        if not self.exists(account_id):
            return Nothing()
        transactions = self._get_transactions(account_id)
        acc = BankAccount(account_id, transactions)
        return Just(acc)

    def _get_transactions(self, account_id: int) -> Transactions:
        cursor = self.connection_pool.get_cursor(self.identifier)
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
