from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as a_repo,
    AccountID,
    Balance
)
from ApplicationService.repositories.transactioncontext import (
    transactioncontext as cntx
)


class GetBalanceUseCase:
    def __init__(self, acc_repository: a_repo, db_context: cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, acc_id: AccountID) -> Balance:
        with self._db_context:
            acc = self._acc_repository.get_by_id(acc_id)
            acc_balance = acc.get_balance()

        return acc_balance
