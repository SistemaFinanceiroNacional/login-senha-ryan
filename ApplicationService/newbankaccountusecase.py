from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as iar,
    ClientID
)
from ApplicationService.repositories.transactioncontext import (
    transactioncontext as cntx
)


class NewBankAccountUseCase:
    def __init__(self, acc_repository: iar, db_context: cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, client_id: ClientID) -> bool:
        with self._db_context:
            self._acc_repository.add_account(client_id)

        return not self._db_context.get_errors()
