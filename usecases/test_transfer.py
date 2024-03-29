from usecases.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from usecases.transfer import (
    TransferFundsUseCase
)
from domain.transaction import create_transaction
from domain.bankaccount import (
    BankAccount,
    InvalidValueToTransfer
)
from fake_config.fakes import (
    ContasFake,
    FakeContext
)

default_id = 1
ryan_id = 2
joao_id = 3


def test_transfer_correct():
    t = create_transaction(default_id, ryan_id, 300)
    ryan_acc = BankAccount(ryan_id, [t])
    joao_acc = BankAccount(joao_id, [])
    context = FakeContext()

    acc_repository = ContasFake({ryan_id: [ryan_acc], joao_id: [joao_acc]}, {})

    use_case = TransferFundsUseCase(acc_repository, context)

    assert use_case.execute(ryan_id, joao_id, 150)


def test_transfer_correct_ryan_balance():
    t = create_transaction(default_id, ryan_id, 100)
    ryan_acc = BankAccount(ryan_id, [t])
    joao_acc = BankAccount(joao_id, [])
    context = FakeContext()

    acc_repository = ContasFake({ryan_id: [ryan_acc], joao_id: [joao_acc]}, {})

    use_case = TransferFundsUseCase(acc_repository, context)
    use_case.execute(ryan_id, joao_id, 100)

    maybe_acc = acc_repository.get_by_id(ryan_id)
    ryan_balance = maybe_acc.map(lambda acc: acc.get_balance())\
        .or_else(lambda: None)
    assert ryan_balance == 0


def test_transfer_zero_amount():
    t = create_transaction(default_id, ryan_id, 100)
    ryan_acc = BankAccount(ryan_id, [t])
    joao_acc = BankAccount(joao_id, [])
    context = FakeContext()

    acc_repository = ContasFake({ryan_id: [ryan_acc], joao_id: [joao_acc]}, {})

    use_case = TransferFundsUseCase(acc_repository, context)

    try:
        use_case.execute(ryan_id, joao_id, 0)
        assert False

    except InvalidValueToTransfer as e:
        assert str(e) == "0 is a non-positive value to transfer."


def test_transfer_negative_amount():
    t = create_transaction(default_id, ryan_id, 100)
    ryan_acc = BankAccount(ryan_id, [t])
    joao_acc = BankAccount(joao_id, [])
    context = FakeContext()

    acc_repository = ContasFake({ryan_id: [ryan_acc], joao_id: [joao_acc]}, {})

    use_case = TransferFundsUseCase(acc_repository, context)

    try:
        use_case.execute(ryan_id, joao_id, -50)
        assert False

    except InvalidValueToTransfer as e:
        assert str(e) == "-50 is a non-positive value to transfer."


def test_transfer_not_existing_login_destiny():
    t = create_transaction(default_id, ryan_id, 100)
    ryan_acc = BankAccount(ryan_id, [t])
    joao_acc = BankAccount(joao_id, [])
    context = FakeContext()

    acc_repository = ContasFake({ryan_id: [ryan_acc], joao_id: [joao_acc]}, {})

    use_case = TransferFundsUseCase(acc_repository, context)

    wrong_id = 4
    try:
        use_case.execute(ryan_id, wrong_id, 50)
        assert False
    except AccountDoesNotExistsError as e:
        assert str(e) == "Account 4 does not exists."
