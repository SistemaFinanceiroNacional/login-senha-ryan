import maybe
import password
from ApplicationService.contexterrors.accountdoesnotexistserror import AccountDoesNotExistsError
from ApplicationService.transferFundsBetweenAccountsUseCase import transferFundsBetweenAccountsUseCase
from ApplicationService.transactioncontext import transactioncontext
from ApplicationService.repositories.externalaccountsrepository import externalAccountsRepository
from drivers.Cli.test_command_line_interface import contasFake, fake_context
from ApplicationService.externalAccount import externalAccount
from ApplicationService.internalAccount import internalAccount, invalidValueToTransfer


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

    def update(self, login: str, balance: float):
        if login in self.accounts:
            account = self.accounts.get(login)
            account.balanceIncrement = balance
            self.accounts[login] = account

    def add_account(self, login, account):
        self.accounts[login] = account


def test_transfer_correct():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 300)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsBetweenAccountsUseCase(intRepository, extRepository, context)

    assert useCase.execute(intAccount, "joao", 150)


def test_transfer_correct2():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 100)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsBetweenAccountsUseCase(intRepository, extRepository, context)
    useCase.execute(intAccount, "joao", 100)

    assert intRepository.actualAccounts["ryan"].m_balance == 0 and extRepository.accounts["joao"].balanceIncrement == 100


def test_transfer_zero_amout():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 100)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsBetweenAccountsUseCase(intRepository, extRepository, context)

    try:
        useCase.execute(intAccount, "joao", 0)
        assert False

    except invalidValueToTransfer as e:
        assert e.value == 0

def test_transfer_negative_amount():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 100)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsBetweenAccountsUseCase(intRepository, extRepository, context)

    try:
        useCase.execute(intAccount, "joao", -50)
        assert False

    except invalidValueToTransfer as e:
        assert e.value == -50

def test_transfer_not_existing_login_destiny():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 100)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsBetweenAccountsUseCase(intRepository, extRepository, context)

    try:
        useCase.execute(intAccount, "henio", 50)
        assert False
    except AccountDoesNotExistsError as e:
        assert e.destinyLogin == "henio"


if __name__ == "__main__":
    test_transfer_correct2()
