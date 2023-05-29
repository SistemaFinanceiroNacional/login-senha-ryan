from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from ApplicationService.TransferFundsUseCase import (
    TransferFundsUseCase
)
from Domain.transaction import create_transaction
from Domain.account import (
    Account,
    invalidValueToTransfer
)
from fake_config.fakes import (
    contasFake,
    fake_context
)

defaultID = 1
ryanID = 2
joaoID = 3


def test_transfer_correct():
    t = create_transaction(defaultID, ryanID, 300)
    ryan_acc = Account(ryanID, [t])
    joao_acc = Account(joaoID, [])
    context = fake_context()

    acc_repository = contasFake({ryanID: [ryan_acc], joaoID: [joao_acc]}, {})

    useCase = TransferFundsUseCase(acc_repository, context)

    assert useCase.execute(ryanID, joaoID, 150)


def test_transfer_correct_ryan_balance():
    t = create_transaction(defaultID, ryanID, 100)
    ryan_acc = Account(ryanID, [t])
    joao_acc = Account(joaoID, [])
    context = fake_context()

    acc_repository = contasFake({ryanID: [ryan_acc], joaoID: [joao_acc]}, {})

    useCase = TransferFundsUseCase(acc_repository, context)
    useCase.execute(ryanID, joaoID, 100)

    ryan_balance = acc_repository.get_balance(ryanID)
    assert ryan_balance == 0


def test_transfer_zero_amount():
    t = create_transaction(defaultID, ryanID, 100)
    ryan_acc = Account(ryanID, [t])
    joao_acc = Account(joaoID, [])
    context = fake_context()

    acc_repository = contasFake({ryanID: [ryan_acc], joaoID: [joao_acc]}, {})

    useCase = TransferFundsUseCase(acc_repository, context)

    try:
        useCase.execute(ryanID, joaoID, 0)
        assert False

    except invalidValueToTransfer as e:
        assert e.value == 0


def test_transfer_negative_amount():
    t = create_transaction(defaultID, ryanID, 100)
    ryan_acc = Account(ryanID, [t])
    joao_acc = Account(joaoID, [])
    context = fake_context()

    acc_repository = contasFake({ryanID: [ryan_acc], joaoID: [joao_acc]}, {})

    useCase = TransferFundsUseCase(acc_repository, context)

    try:
        useCase.execute(ryanID, joaoID, -50)
        assert False

    except invalidValueToTransfer as e:
        assert e.value == -50


def test_transfer_not_existing_login_destiny():
    t = create_transaction(defaultID, ryanID, 100)
    ryan_acc = Account(ryanID, [t])
    joao_acc = Account(joaoID, [])
    context = fake_context()

    acc_repository = contasFake({ryanID: [ryan_acc], joaoID: [joao_acc]}, {})

    useCase = TransferFundsUseCase(acc_repository, context)

    wrong_id = 4
    try:
        useCase.execute(ryanID, wrong_id, 50)
        assert False
    except AccountDoesNotExistsError as e:
        assert e.destinyID == 4
