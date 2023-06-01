from typing import Iterable

from Domain.account import Account
from ApplicationService.repositories.identityinterface import identityInterface
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface,
    AccountID,
    Balance, ClientID
)
from Domain.transaction import create_transaction
from ApplicationService.repositories.transactioncontext import(
    transactioncontext
)
from ApplicationService.repositories.connectionInterface import connection_pool
from ApplicationService.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface
)
from Infrastructure.authserviceinterface import AuthServiceInterface
from inputIO.inputIO import inputIO
from password import Password as pw
from maybe import maybe, just, nothing


class fake_identity(identityInterface):
    def __init__(self, iden):
        self.iden = iden

    def value(self):
        return self.iden


class fake_connection(connection_pool):
    def __call__(self, *args, **kwargs):
        return self

    def cursor(self):
        return fake_cursor()

    def get_connection(self, identifier):
        pass

    def get_cursor(self, identifier):
        return fake_cursor()

    def refund(self, identifier):
        pass


class fake_cursor:
    def execute(self):
        pass


class fakeContext(transactioncontext):
    def __init__(self):
        self.errors = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_errors(self):
        return self.errors


class inputfake(inputIO):
    def __init__(self, lista):
        self.inputlist = lista
        self.outputlist = []

    def input(self, prompt):
        return self.inputlist.pop()

    def inputoccult(self, prompt):
        return self.inputlist.pop()

    def print(self, prompt):
        self.outputlist.append(prompt)


class clientsFake(ClientsRepositoryInterface):
    def __init__(self, clients: dict):
        self.clients = clients

    def add_client(self, login: str, password: pw) -> bool:
        if login in self.clients:
            return False
        self.clients[login] = password
        return True


class contasFake(AccountsRepositoryInterface):
    def __init__(self, actualAccounts, newAccounts):
        # self.actualAccounts: set[ClientID, tuple[str, str]] = actualAccounts
        self.actualAccounts: dict[ClientID, list[Account]] = actualAccounts
        self.newAccounts = newAccounts

    def add_client(self, new_login, new_password: pw):
        if new_login not in self.actualAccounts:
            self.actualAccounts[new_login] = (new_password, 0)
            return True
        else:
            return False

    # def update(self, intAccount: Account):
    #     login = intAccount.get_id()
    #     balance = intAccount.get_balance()
    #
    #     if login in self.actualAccounts:
    #         account = self.actualAccounts.get(login)
    #         account._balance = balance
    #         self.actualAccounts[login] = account

    def exists(self, login):
        return login in self.actualAccounts

    def update(self, account: Account):
        pass

    def get_balance(self, account_id: AccountID) -> Balance:
        return self.get_by_id(account_id).get_balance()

    def get_by_id(self, account_id: AccountID) -> Account:
        for clientID in self.actualAccounts:
            for acc in self.actualAccounts[clientID]:
                if acc.get_id() == account_id:
                    return acc

    def get_by_client_id(self, client_id: ClientID) -> Iterable[AccountID]:
        accounts_id = [acc.get_id() for acc in self.actualAccounts[client_id]]
        return accounts_id

def existing_pedros_account():
    t = create_transaction(2, 3, 400)
    return contasFake({"pedro": ("abc123", [t])}, {})


def waiting_pedro_account():
    return contasFake({}, {"pedro": "abc123"})


class fake_context(transactioncontext):
    def __init__(self):
        self.errors = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_errors(self):
        return self.errors


class fakeSocket:
    def __init__(self, content):
        self.content = content

    def recv(self, bufsize):
        requiredContent = self.content[0:bufsize]
        self.content = self.content[bufsize:]
        return requiredContent


class fake_authService(AuthServiceInterface):
    def __init__(self):
        self.accounts = {}

    def authenticate(self, username: str, password: str) -> maybe[int]:
        if username in self.accounts.keys():
            return just(self.accounts[username][1])
        else:
            return nothing()
