from typing import NamedTuple

import pytest

from domain.commontypes.types import AccountID, ClientID
from infrastructure.accountsrepository import AccountsRepository
from infrastructure.authservicedb import AuthServiceDB
from infrastructure.clientsrepository import ClientsRepository
from infrastructure.connection_pool import (
    PostgresqlConnectionPool,
    psycopg2_create_connection
)
from infrastructure.dbtransactioncontext import DBTransactionContext
from infrastructure.threadIdentity import ThreadIdentity
from password import Password
from usecases.deposit import DepositUseCase
from usecases.get_accounts import GetAccountsUseCase
from usecases.get_balance import GetBalanceUseCase
from usecases.get_transactions import GetTransactionsUseCase
from usecases.register_client import RegisterClientUseCase

PASSWORD = "secret"


class Client(NamedTuple):
    id: ClientID
    account: AccountID


class Bank:
    """The use cases wired to the real infrastructure, as the drivers do.
    Scenarios are built only through business operations."""

    def __init__(self):
        pool = PostgresqlConnectionPool(psycopg2_create_connection, 1)
        identity = ThreadIdentity()
        accounts = AccountsRepository(pool, identity)
        clients = ClientsRepository(pool, identity)
        context = DBTransactionContext(pool, identity)

        self.register_client = RegisterClientUseCase(
            clients, context, Password
        )
        self.auth = AuthServiceDB(context, pool, identity)
        self.get_accounts = GetAccountsUseCase(accounts, context)
        self.get_balance = GetBalanceUseCase(accounts, context)
        self.get_transactions = GetTransactionsUseCase(accounts, context)
        self.deposit = DepositUseCase(accounts, context)

    def open_client(self, login: str) -> Client:
        assert self.register_client.execute(login, PASSWORD)
        not_logged = AssertionError(f"{login} could not log in")
        client_id = self.auth.authenticate(login, PASSWORD)\
            .or_else_throw(not_logged)
        [account] = self.get_accounts.execute(client_id)
        return Client(client_id, account)


@pytest.fixture
def bank(database) -> Bank:
    return Bank()
