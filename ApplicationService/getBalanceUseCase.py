from Infrastructure.accountsrepository import (
    AccountsRepositoryInterface as iar
)
from ApplicationService.repositories.transactioncontext import (
    transactioncontext as cntx
)

AccountID = int
Balance = float


class GetBalanceUseCase:
    def __init__(self, acc_repository: iar, trans_context: cntx):
        self._acc_repository = acc_repository
        self._trans_context = trans_context

    def execute(self, acc_id: AccountID) -> Balance:
        with self._trans_context:
            acc_balance = self._acc_repository.get_balance(acc_id)
        return acc_balance
