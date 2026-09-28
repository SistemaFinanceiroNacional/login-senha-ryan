from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as tContext
)
from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as accRepo,
    BankAccount
)
from usecases.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from domain.amount import Amount
from domain.commontypes.types import AccountID, ClientID
from usecases.contexterrors.sameaccounttransfererror import (
    SameAccountTransferError
)


class TransferFundsUseCase:
    def __init__(self,
                 acc_repository: accRepo,
                 transactional_context: tContext
                 ):
        self.acc_repository = acc_repository
        self.transactional_context = transactional_context

    def execute(self,
                client_id: ClientID,
                acc_id: AccountID,
                dest_id: AccountID,
                amount: Amount
                ) -> bool:
        """Moves money from one of the client's accounts to another
        account. An account the client does not own is, to them, an
        account that does not exist."""
        if acc_id == dest_id:
            raise SameAccountTransferError(acc_id)
        with self.transactional_context:
            client_accounts = self.acc_repository.get_by_client_id(client_id)
            if acc_id not in client_accounts:
                raise AccountDoesNotExistsError(acc_id)
            get_existence = self.acc_repository.exists
            both_exists = get_existence(acc_id) and get_existence(dest_id)
            if not both_exists:
                raise AccountDoesNotExistsError(dest_id)

            maybe_account = self.acc_repository.get_by_id(acc_id)

            def transfer_to(account: BankAccount):
                account.transfer(dest_id, amount)
                self.acc_repository.update(account)

            maybe_account.run(transfer_to)

        if self.transactional_context.get_errors():
            return False
        else:
            return True
