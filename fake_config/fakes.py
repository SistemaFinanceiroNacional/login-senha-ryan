from typing import Iterable, Tuple, List

from domain.bankaccount import BankAccount
from infrastructure.identityinterface import IdentityInterface
from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface,
    AccountID,
    ClientID
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)
from infrastructure.connectionInterface import (
    ConnectionPool,
    Connection,
    Cursor
)
from maybe import Maybe, Just, Nothing


AccountsByClient = dict[ClientID, list[BankAccount]]


class FakeIdentity(IdentityInterface):
    def __init__(self, iden):
        self.iden = iden

    def value(self):
        return self.iden


class FakeConnection(Connection):
    def cursor(self) -> Cursor:
        return FakeCursor()

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class FakeConnectionPool(ConnectionPool):
    def __call__(self, *args, **kwargs):
        return self

    def get_connection(self, identifier):
        pass

    def get_cursor(self, identifier):
        return FakeCursor()

    def refund(self, identifier):
        pass


class FakeCursor(Cursor):
    def execute(self):
        pass

    def fetchone(self) -> None | Tuple:
        return None

    def fetchall(self) -> List:
        return []


class FakeContext(TransactionContextInterface):
    def __init__(self):
        self.errors = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_errors(self):
        return self.errors


class ContasFake(AccountsRepositoryInterface):
    def __init__(self, actual_accounts, new_accounts):
        self.actual_accounts: AccountsByClient = actual_accounts
        self.new_accounts = new_accounts
        self._accounts = 0

    def add_account(self, client_id):
        if client_id in self.actual_accounts:
            self._accounts += 1
            new_account = BankAccount(self._accounts, [])
            self.actual_accounts[client_id].append(new_account)
            return True
        else:
            return False

    def exists(self, account_id):
        for client_id in self.actual_accounts:
            for acc in self.actual_accounts[client_id]:
                if acc.get_id() == account_id:
                    return True
        return False

    def update(self, account: BankAccount):
        pass

    def get_by_id(self, account_id: AccountID) -> Maybe[BankAccount]:
        for client_id in self.actual_accounts:
            for acc in self.actual_accounts[client_id]:
                if acc.get_id() == account_id:
                    return Just(acc)
        return Nothing()

    def get_by_client_id(self, client_id: ClientID) -> Iterable[AccountID]:
        accounts_id = [acc.get_id() for acc in self.actual_accounts[client_id]]
        return accounts_id


class FakeSocket:
    def __init__(self, content):
        self.content = content

    def recv(self, bufsize):
        required_content = self.content[0:bufsize]
        self.content = self.content[bufsize:]
        return required_content
