from ApplicationService.repositories.internalaccountsrepository import internalAccountsRepository
from drivers.Cli import command_line_interface
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.transactioncontext import transactioncontext
from ApplicationService.transferFundsBetweenAccountsUseCase import transferFundsBetweenAccountsUseCase
from ApplicationService.repositories.externalaccountsrepository import externalAccountsRepository
from ApplicationService.externalAccount import externalAccount
from ApplicationService.openAccountUseCase import openAccountUseCase
import maybe
import password
from ApplicationService.internalAccount import internalAccount
import psycopg2


class inputfake:
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
        if login in self.actualAccounts and str(hashsenha) == str(user_password):
            return maybe.just(internalAccount(login, user_password, self.actualAccounts[login][1]))
        else:
            return maybe.nothing()

    def add_account(self, new_login, new_password):
        hashsenha = password.password(new_password)
        if new_login not in self.actualAccounts:
            self.actualAccounts[new_login] = (hashsenha, 0)
            return True
        else:
            return False

        # return new_login  and new_login in self.newAccounts and str(hashsenha) == str(new_password)


def existing_pedros_account():
    return contasFake(actualAccounts={"pedro": ("abc123", "400")}, newAccounts={})


def waiting_pedro_account():
    return contasFake(newAccounts={"pedro": "abc123"}, actualAccounts={})


class fake_context(transactioncontext):
    def __init__(self):
        self.errors = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_errors(self):
        return self.errors


def test_main_with_repl():
    context = fake_context()
    c = existing_pedros_account()
    extC = contasExternasFake({})

    loginCase = loginUseCase(c, context)
    transferCase = transferFundsBetweenAccountsUseCase(c, extC, context)
    openCase = openAccountUseCase(c, context)

    i = inputfake(["logout", "balance", "abc123", "pedro", "1"])

    command_line_interface.main(i, loginCase, transferCase, openCase)
    assert i.outputlist[0] == "400"


def test_main_choose_2_already_exist():
    context = fake_context()
    c = waiting_pedro_account()
    extC = contasExternasFake({})

    loginCase = loginUseCase(c, context)
    transferCase = transferFundsBetweenAccountsUseCase(c, extC, context)
    openCase = openAccountUseCase(c, context)

    i = inputfake(["abc123", "pedro", "2"])

    command_line_interface.main(i, loginCase, transferCase, openCase)
    assert i.outputlist[0] == "Your account has been successfully created!"


def test_verify_correct_content_using_different_password():
    context = fake_context()
    c = existing_pedros_account()
    extC = contasExternasFake({})

    loginCase = loginUseCase(c, context)
    transferCase = transferFundsBetweenAccountsUseCase(c, extC, context)
    openCase = openAccountUseCase(c, context)

    i = inputfake(["abc123", "pedro", "2"])

    command_line_interface.main(i, loginCase, transferCase, openCase)

    assert i.outputlist[0] == "Account already exists. Try another username."
