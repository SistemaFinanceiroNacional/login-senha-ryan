from Infrastructure.accountsrepository import (
    AccountsRepositoryInterface as iar
)
from ApplicationService.repositories.transactioncontext import (
    transactioncontext as cntx
)

ClientID = int


class GetAccountsUseCase:
    def __init__(self, acc_repository: iar, trans_context: cntx):
        self._acc_repository = acc_repository
        self._trans_context = trans_context

    def execute(self, client_id: ClientID):
        with self._trans_context:
            acc_iter = self._acc_repository.get_by_client_id(client_id)
        return acc_iter