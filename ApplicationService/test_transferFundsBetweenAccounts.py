import password
from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from ApplicationService.transferFundsUseCase import (
    transferFundsUseCase
)
from ApplicationService.external_account import externalAccount
from ApplicationService.internal_account import (
    internalAccount,
    invalidValueToTransfer
)
from fake_config.fakes import (
    fakeExternalRepository,
    contasFake,
    fake_context
)


def test_transfer_correct():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 300)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsUseCase(intRepository, extRepository, context)

    assert useCase.execute(intAccount, "joao", 150)


def test_transfer_correct_ryan_balance():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 100)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsUseCase(intRepository, extRepository, context)
    useCase.execute(intAccount, "joao", 100)

    ryan_balance = intRepository.actualAccounts["ryan"]._balance

    assert ryan_balance == 0


def test_transfer_correct_veryfing_joaos_balance():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 100)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsUseCase(intRepository, extRepository, context)
    useCase.execute(intAccount, "joao", 100)

    balance_increment_joao = extRepository.accounts["joao"]._balanceIncrement

    assert balance_increment_joao == 100


def test_transfer_zero_amount():
    extAccount = externalAccount("joao")
    intAccount = internalAccount("ryan", password.password("abc123"), 100)
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount}, {})
    extRepository = fakeExternalRepository()
    extRepository.add_account("joao", extAccount)

    useCase = transferFundsUseCase(intRepository, extRepository, context)

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

    useCase = transferFundsUseCase(intRepository, extRepository, context)

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

    useCase = transferFundsUseCase(intRepository, extRepository, context)

    try:
        useCase.execute(intAccount, "henio", 50)
        assert False
    except AccountDoesNotExistsError as e:
        assert e.destinyLogin == "henio"
