import password
from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from ApplicationService.transferFundsUseCase import (
    transferFundsUseCase
)
from ApplicationService.transaction import create_transaction
from ApplicationService.internal_account import (
    internalAccount,
    invalidValueToTransfer
)
from fake_config.fakes import (
    contasFake,
    fake_context
)


def test_transfer_correct():
    t = create_transaction("joao", "ryan", 300)
    intAccount = internalAccount("ryan", password.password("abc123"), [t])
    joao_acc = internalAccount("joao", password.password("ab123"), [t])
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount, "joao": joao_acc}, {})

    useCase = transferFundsUseCase(intRepository, context)

    assert useCase.execute(intAccount, "joao", 150)


def test_transfer_correct_ryan_balance():
    t = create_transaction("joao", "ryan", 100)
    intAccount = internalAccount("ryan", password.password("abc123"), [t])
    joao_acc = internalAccount("joao", password.password("ab123"), [t])
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount, "joao": joao_acc}, {})

    useCase = transferFundsUseCase(intRepository, context)
    useCase.execute(intAccount, "joao", 100)

    ryan_balance = intRepository.actualAccounts["ryan"]._balance

    assert ryan_balance == 0


def test_transfer_zero_amount():
    t = create_transaction("joao", "ryan", 100)
    intAccount = internalAccount("ryan", password.password("abc123"), [t])
    joao_acc = internalAccount("joao", password.password("ab123"), [t])
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount, "joao": joao_acc}, {})

    useCase = transferFundsUseCase(intRepository, context)

    try:
        useCase.execute(intAccount, "joao", 0)
        assert False

    except invalidValueToTransfer as e:
        assert e.value == 0


def test_transfer_negative_amount():
    t = create_transaction("joao", "ryan", 100)
    intAccount = internalAccount("ryan", password.password("abc123"), [t])
    joao_acc = internalAccount("joao", password.password("ab123"), [t])
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount, "joao": joao_acc}, {})

    useCase = transferFundsUseCase(intRepository, context)

    try:
        useCase.execute(intAccount, "joao", -50)
        assert False

    except invalidValueToTransfer as e:
        assert e.value == -50


def test_transfer_not_existing_login_destiny():
    t = create_transaction("joao", "ryan", 100)
    intAccount = internalAccount("ryan", password.password("abc123"), [t])
    joao_acc = internalAccount("joao", password.password("ab123"), [t])
    context = fake_context()

    intRepository = contasFake({"ryan": intAccount, "joao": joao_acc}, {})

    useCase = transferFundsUseCase(intRepository, context)

    try:
        useCase.execute(intAccount, "henio", 50)
        assert False
    except AccountDoesNotExistsError as e:
        assert e.destinyLogin == "henio"
