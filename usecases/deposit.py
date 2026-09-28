from domain.amount import Amount
from domain.bankaccount import BankAccount
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
        with self._db_context:
            client_accounts = self._acc_repository.get_by_client_id(client_id)
            if account_id not in client_accounts:
                return False
            maybe_account = self._acc_repository.get_by_id(account_id)
            deposited = maybe_account.map(
                lambda account: self._deposit(account, amount)
            )
            return deposited.or_else(lambda: False)

    def _deposit(self, account: BankAccount, amount: Amount) -> bool:
        account.deposit(amount)
        self._acc_repository.update(account)
        return True
