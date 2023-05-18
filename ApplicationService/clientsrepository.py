from typing import List
from ApplicationService.connection_pool import (
    connection_pool as cpool,
    cursor as c
)
from ApplicationService.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface,
    Client,
    pw
)
from ApplicationService.transaction import (
    Transaction,
    create_transaction_from_raw
)
from maybe import just, nothing, maybe
from ApplicationService.repositories.identityinterface import identityInterface
from ApplicationService.account import Account


class ClientsRepository(ClientsRepositoryInterface):
    def __init__(self, connection_pool: cpool, identifier: identityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def get_by_credentials(self, login: str, password: pw) -> maybe[Client]:
        cursor = self.connection_pool.get_cursor(self.identifier)

        columns = "id, login, password"
        table = "clients"
        conditions = "login=%s AND password=%s"
        query = f"SELECT {columns} FROM {table} WHERE {conditions};"

        cursor.execute(query, (login, str(password)))

        find_login_list = cursor.fetchone()

        if find_login_list is not None:
            c_id, c_login, c_pw = find_login_list
            c_accounts = self._get_client_accounts(c_id, cursor)
            client = Client(c_login, c_pw, c_accounts)
            return just(client)
        return nothing()

    def _get_client_accounts(self, clientID: int, cursor: c) -> List[Account]:
        columns = "account_id"
        table = "clients_accounts"
        conditions = "client_id=%s"
        query = f"SELECT {columns} FROM {table} WHERE {conditions};"

        cursor.execute(query, (clientID,))
        accounts_ids = cursor.fetchall()

        accounts = []
        if accounts_ids:
            for data in accounts_ids:
                acc_id = data[0]
                trans = self._get_transactions(acc_id, cursor)
                acc = Account(acc_id, trans)
                accounts.append(acc)

        return accounts

    def _get_transactions(self, account_id: int, cursor: c) -> List[Transaction]:
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
