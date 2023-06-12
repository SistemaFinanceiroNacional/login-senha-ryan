from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as AccRepo
)
from ApplicationService.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)
from Domain.account import Amount
from Domain.CommonTypes.types import AccountID


class GetBalanceUseCase:
    def __init__(self, acc_repository: AccRepo, db_context: Cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, acc_id: AccountID) -> Amount:
        with self._db_context:
            acc = self._acc_repository.get_by_id(acc_id)
            acc_balance = acc.get_balance()

        return acc_balance
