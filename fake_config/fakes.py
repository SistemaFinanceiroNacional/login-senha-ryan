from maybe import just, nothing, maybe
from ApplicationService.account import Account
from ApplicationService.repositories.identityinterface import identityInterface
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface
)
from ApplicationService.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface
)
from ApplicationService.client import Client
from ApplicationService.transaction import create_transaction
from ApplicationService.transactioncontext import transactioncontext
from inputIO.inputIO import inputIO
from password import password as pw


class fake_identity(identityInterface):
    def __init__(self, iden):
        self.iden = iden

    def value(self):
        return self.iden


class fake_connection:
    def cursor(self):
        return fake_cursor()


class fake_cursor:
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


class contasFake(AccountsRepositoryInterface):
    def __init__(self, actualAccounts, newAccounts):
        self.actualAccounts = actualAccounts
        self.newAccounts = newAccounts

    def add_account(self, new_login, new_password: pw):
        if new_login not in self.actualAccounts:
            self.actualAccounts[new_login] = (new_password, 0)
            return True
        else:
            return False

    def update_balance(self, intAccount: Account):
        login = intAccount.get_id()
        balance = intAccount.get_balance()

        if login in self.actualAccounts:
            account = self.actualAccounts.get(login)
            account._balance = balance
            self.actualAccounts[login] = account

    def exists(self, login):
        return login in self.actualAccounts

    def update(self, account: Account):
        pass


class clientsFake(ClientsRepositoryInterface):
    def __init__(self, clients: dict[str, Client]):
        self.c = clients

    def get_by_credentials(self, login: str, password: pw) -> maybe[Client]:
        return just(self.c[login]) if login in self.c else nothing()


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
