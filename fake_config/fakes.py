from typing import Iterable

from Domain.account import Account
from Infrastructure.identityinterface import IdentityInterface
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface,
    AccountID,
    ClientID
)
from Domain.transaction import create_transaction
from ApplicationService.repositories.transactioncontextinterface import (
    TransactionContextInterface
)
from Infrastructure.connectionInterface import ConnectionPool
from ApplicationService.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface
)
from Infrastructure.authserviceinterface import AuthServiceInterface
from inputIO.inputIO import InputIO
from password import Password as passW
from maybe import Maybe, Just, Nothing


class FakeIdentity(IdentityInterface):
    def __init__(self, iden):
        self.iden = iden

    def value(self):
        return self.iden


class FakeConnection(ConnectionPool):
    def __call__(self, *args, **kwargs):
        return self

    def cursor(self):
        return FakeCursor()

    def get_connection(self, identifier):
        pass

    def get_cursor(self, identifier):
        return FakeCursor()

    def refund(self, identifier):
        pass


class FakeCursor:
    def execute(self):
        pass


class FakeContext(TransactionContextInterface):
    def __init__(self):
        self.errors = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_errors(self):
        return self.errors


class InputFake(InputIO):
    def __init__(self, lista):
        self.inputlist = lista
        self.outputlist = []

    def input(self, prompt):
        return self.inputlist.pop()

    def inputoccult(self, prompt):
        return self.inputlist.pop()

    def print(self, prompt):
        self.outputlist.append(prompt)


class ClientsFake(ClientsRepositoryInterface):
    def __init__(self, clients: dict):
        self.clients = clients

    def add_client(self, login: str, password: passW) -> bool:
        if login in self.clients:
            return False
        self.clients[login] = password
        return True


class ContasFake(AccountsRepositoryInterface):
    def __init__(self, actual_accounts, new_accounts):
        self.actualAccounts: dict[ClientID, list[Account]] = actual_accounts
        self.newAccounts = new_accounts

    def add_client(self, new_login, new_password: passW):
        if new_login not in self.actualAccounts:
            self.actualAccounts[new_login] = (new_password, 0)
            return True
        else:
            return False

    def exists(self, login):
        return login in self.actualAccounts

    def update(self, account: Account):
        pass

    def get_by_id(self, account_id: AccountID) -> Account:
        for client_id in self.actualAccounts:
            for acc in self.actualAccounts[client_id]:
                if acc.get_id() == account_id:
                    return acc

    def get_by_client_id(self, client_id: ClientID) -> Iterable[AccountID]:
        accounts_id = [acc.get_id() for acc in self.actualAccounts[client_id]]
        return accounts_id


def existing_pedros_account():
    t = create_transaction(2, 3, 400)
    return ContasFake({"pedro": ("abc123", [t])}, {})


def waiting_pedro_account():
    return ContasFake({}, {"pedro": "abc123"})


class FakeSocket:
    def __init__(self, content):
        self.content = content

    def recv(self, bufsize):
        required_content = self.content[0:bufsize]
        self.content = self.content[bufsize:]
        return required_content


class FakeAuthService(AuthServiceInterface):
    def __init__(self, accounts: dict):
        self.accounts = accounts

    def authenticate(self, username: str, password: str) -> Maybe[int]:
        if username in self.accounts:
            return Just(self.accounts[username][1])
        else:
            return Nothing()
