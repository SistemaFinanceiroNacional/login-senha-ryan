from typing import Iterable, List
from maybe import Maybe, Just, Nothing
from domain.amount import Amount
from domain.transaction import Transaction
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
        # The FLOAT column is still written so that a previous version of
        # the application, which only reads it, keeps working (#116).
        insert_transaction = \
            "INSERT INTO transactions " \
            "(uuid, debit_account, credit_account, value, date) " \
            "VALUES (%s, %s, %s, %s, %s) ON CONFLICT (uuid) DO NOTHING;"
        insert_amount = \
            "INSERT INTO transaction_amounts (transaction_uuid, amount) " \
            "VALUES (%s, %s) ON CONFLICT (transaction_uuid) DO NOTHING;"

        for t in acc.get_transactions():
            amount = t.value.to_decimal()
            cursor.execute(
                insert_transaction, (t.id, t.d_acc, t.c_acc, amount, t.date)
            )
            cursor.execute(insert_amount, (t.id, amount))

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
        # Rows written by a previous version have no exact amount yet: fall
        # back to the FLOAT column rounded to cents.
        query = \
            "SELECT t.uuid, t.debit_account, t.credit_account, " \
            "COALESCE(ta.amount, round(t.value::numeric, 2)), t.date " \
            "FROM transactions t " \
            "LEFT JOIN transaction_amounts ta " \
            "ON ta.transaction_uuid = t.uuid " \
            "WHERE t.debit_account = %s OR t.credit_account = %s;"
        cursor.execute(query, (account_id, account_id))
        return [
            Transaction(t_id, d_acc, c_acc, Amount(amount), date)
            for t_id, d_acc, c_acc, amount, date in cursor.fetchall()
        ]
