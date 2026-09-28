from domain.bankaccount import Amount
from domain.commontypes.types import AccountID, ClientID
from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as AccRepo
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)


class DepositUseCase:
    """Cash deposited by a client into one of their own accounts, e.g.
    through an ATM."""

    def __init__(self, acc_repository: AccRepo, db_context: Cntx):
        self._acc_repository = acc_repository
        self._db_context = db_context

    def execute(self,
                client_id: ClientID,
                account_id: AccountID,
                amount: Amount
                ) -> bool:
        raise NotImplementedError
