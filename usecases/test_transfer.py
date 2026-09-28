from usecases.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from usecases.transfer import (
    TransferFundsUseCase
)
from domain.amount import Amount
from domain.money import Money
from domain.transaction import create_transaction
from domain.bankaccount import BankAccount
from fake_config.fakes import (
    ContasFake,
    FakeContext
)

default_id = 1
ryan_id = 2
joao_id = 3


def test_transfer_correct():
    t = create_transaction(default_id, ryan_id, Amount(300))
    ryan_acc = BankAccount(ryan_id, [t])
    joao_acc = BankAccount(joao_id, [])
    context = FakeContext()

    acc_repository = ContasFake({ryan_id: [ryan_acc], joao_id: [joao_acc]}, {})

    use_case = TransferFundsUseCase(acc_repository, context)

    assert use_case.execute(ryan_id, ryan_id, joao_id, Amount(150))


def test_transfer_correct_ryan_balance():
    t = create_transaction(default_id, ryan_id, Amount(100))
    ryan_acc = BankAccount(ryan_id, [t])
    joao_acc = BankAccount(joao_id, [])
    context = FakeContext()

    acc_repository = ContasFake({ryan_id: [ryan_acc], joao_id: [joao_acc]}, {})

    use_case = TransferFundsUseCase(acc_repository, context)
    use_case.execute(ryan_id, ryan_id, joao_id, Amount(100))

    maybe_acc = acc_repository.get_by_id(ryan_id)
    ryan_balance = maybe_acc.map(lambda acc: acc.get_balance())\
        .or_else(lambda: None)
    assert ryan_balance == Money(0)


def test_transfer_not_existing_login_destiny():
    t = create_transaction(default_id, ryan_id, Amount(100))
    ryan_acc = BankAccount(ryan_id, [t])
    joao_acc = BankAccount(joao_id, [])
    context = FakeContext()

    acc_repository = ContasFake({ryan_id: [ryan_acc], joao_id: [joao_acc]}, {})

    use_case = TransferFundsUseCase(acc_repository, context)

    wrong_id = 4
    try:
        use_case.execute(ryan_id, ryan_id, wrong_id, Amount(50))
        assert False
    except AccountDoesNotExistsError as e:
        assert str(e) == "Account 4 does not exists."
