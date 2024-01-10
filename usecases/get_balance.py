from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as AccRepo
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)
from domain.bankaccount import Amount
from domain.commontypes.types import AccountId
from maybe import Maybe


class GetBalanceUseCase:
    def __init__(self, acc_repository: AccRepo, db_context: Cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self, acc_id: AccountId) -> Maybe[Amount]:
        with self._db_context:
            maybe_acc = self._acc_repository.get_by_id(acc_id)

        acc_balance = maybe_acc.map(lambda acc: acc.get_balance())
        return acc_balance
