from fake_config.fakes import ContasFake, FakeContext
from usecases.get_transactions import GetTransactionsUseCase
from maybe import is_just, is_nothing


def test_existing_account():
    cntx = FakeContext()
    acc_repo = ContasFake({1: []}, {})
    acc_repo.add_account(1)

    use_case = GetTransactionsUseCase(acc_repo, cntx)
    assert is_just(use_case.execute(1))


def test_non_existing_account():
    cntx = FakeContext()
    acc_repo = ContasFake({1: []}, {})
    acc_repo.add_account(1)

    use_case = GetTransactionsUseCase(acc_repo, cntx)
    assert is_nothing(use_case.execute(2))
