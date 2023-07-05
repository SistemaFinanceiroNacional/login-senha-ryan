from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as AccRepo
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)
from domain.commontypes.types import ClientID


class NewBankAccountUseCase:
    def __init__(self, acc_repository: AccRepo, db_context: Cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, client_id: ClientID) -> bool:
        with self._db_context:
            self._acc_repository.add_account(client_id)

        return not self._db_context.get_errors()
