import uuid

from fake_config.fakes import ContasFake, FakeContext
from usecases.get_transactions import GetTransactionsUseCase
from maybe import is_just, is_nothing


def test_existing_account():
    cntx = FakeContext()
    client_id = 1
    acc_repo = ContasFake({client_id: []}, {})
    acc_repo.add_account(client_id)

    acc_id = acc_repo.get_by_client_id(client_id).__iter__().__next__()

    use_case = GetTransactionsUseCase(acc_repo, cntx)
    assert is_just(use_case.execute(acc_id))


def test_non_existing_account():
    cntx = FakeContext()
    client_id = 1
    acc_repo = ContasFake({client_id: []}, {})
    acc_repo.add_account(client_id)

    acc_id = uuid.uuid4()

    use_case = GetTransactionsUseCase(acc_repo, cntx)
    assert is_nothing(use_case.execute(acc_id))
