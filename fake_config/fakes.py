import maybe
import password
from ApplicationService.external_account import externalAccount
from ApplicationService.internal_account import internalAccount
from ApplicationService.repositories.externalaccountsrepository\
    import externalAccountsRepository
from ApplicationService.repositories.identity import identity
from ApplicationService.repositories.internalaccountsrepository\
    import internalAccountsRepository
from ApplicationService.transactioncontext import transactioncontext
from inputIO.inputIO import inputIO


class fake_identity(identity):
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


class fakeExternalRepository(externalAccountsRepository):
    def __init__(self):
        self.accounts = dict()

    def get_by_login(self, login: str):
        if login in self.accounts:
            account = self.accounts.get(login)
            return maybe.just(account)
        return maybe.nothing()

    def update(self, extAccount: externalAccount):
        login = extAccount.get_login()
        balance = extAccount.get_increment_balance()

        if login in self.accounts:
            account = self.accounts.get(login)
            account.balanceIncrement = balance
            self.accounts[login] = account

    def add_account(self, login, account):
        self.accounts[login] = account


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


class contasExternasFake(externalAccountsRepository):
    def __init__(self, actualAccounts: dict[str, externalAccount]):
        self.actualAccounts: dict = actualAccounts

    def get_by_login(self, login: str) -> maybe.maybe:
        if login in self.actualAccounts:
            return maybe.just(externalAccount(login))
        else:
            return maybe.nothing()


class contasFake(internalAccountsRepository):
    def __init__(self, actualAccounts, newAccounts):
        self.actualAccounts = actualAccounts
        self.newAccounts = newAccounts

    def authentication(self, login, user_password):
        hashsenha = password.password(self.actualAccounts[login][0])
        password_comparison = str(hashsenha) == str(user_password)
        if login in self.actualAccounts and password_comparison:
            balance = self.actualAccounts[login][1]
            return maybe.just(internalAccount(login, user_password, balance))
        else:
            return maybe.nothing()

    def add_account(self, new_login, new_password):
        hashsenha = password.password(new_password)
        if new_login not in self.actualAccounts:
            self.actualAccounts[new_login] = (hashsenha, 0)
            return True
        else:
            return False

    def update_balance(self, intAccount: internalAccount):
        login = intAccount.get_login()
        balance = intAccount.get_balance()

        if login in self.actualAccounts:
            account = self.actualAccounts.get(login)
            account._balance = balance
            self.actualAccounts[login] = account


def existing_pedros_account():
    return contasFake({"pedro": ("abc123", "400")}, {})


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
