from typing import Iterable
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)
from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as AccRepo
)
from domain.commontypes.types import (
    AccountID,
    ClientID
)


class GetAccountsUseCase:
    def __init__(self, acc_repository: AccRepo, db_context: Cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, client_id: ClientID) -> Iterable[AccountID]:
        with self._db_context:
            acc_iter = self._acc_repository.get_by_client_id(client_id)

        return acc_iter
