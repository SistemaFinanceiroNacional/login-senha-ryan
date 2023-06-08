from typing import Iterable
from ApplicationService.repositories.transactioncontextinterface import (
    TransactionContextInterface as cntx
)
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as a_repo
)
from Domain.CommonTypes.types import (
    AccountID,
    ClientID
)


class GetAccountsUseCase:
    def __init__(self, acc_repository: a_repo, db_context: cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, client_id: ClientID) -> Iterable[AccountID]:
        with self._db_context:
            acc_iter = self._acc_repository.get_by_client_id(client_id)

        return acc_iter
