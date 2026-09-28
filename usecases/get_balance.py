from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as AccRepo
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)
from domain.bankaccount import Money
from domain.commontypes.types import AccountID, ClientID
from maybe import Maybe, Nothing


class GetBalanceUseCase:
    def __init__(self, acc_repository: AccRepo, db_context: Cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self,
                client_id: ClientID,
                acc_id: AccountID
                ) -> Maybe[Money]:
        with self._db_context:
            client_accounts = self._acc_repository.get_by_client_id(client_id)
            if acc_id not in client_accounts:
                return Nothing()
            maybe_acc = self._acc_repository.get_by_id(acc_id)

        acc_balance = maybe_acc.map(lambda acc: acc.get_balance())
        return acc_balance
