from ApplicationService.repositories.transactioncontextinterface import (
    TransactionContextInterface as tContext
)
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as accRepo,
    Account
)
from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from Domain.account import Amount
from Domain.CommonTypes.types import AccountID


class TransferFundsUseCase:
    def __init__(self,
                 acc_repository: accRepo,
                 transactional_context: tContext
                 ):
        self.acc_repository = acc_repository
        self.transactional_context = transactional_context

    def execute(self,
                acc_id: AccountID,
                dest_id: AccountID,
                amount: Amount
                ) -> bool:
        with self.transactional_context:
            existence = self.acc_repository.exists
            both_existence = existence(acc_id) and existence(dest_id)
            if not both_existence:
                raise AccountDoesNotExistsError(dest_id)

            maybe_account = self.acc_repository.get_by_id(acc_id)

            def transfer_to(account: Account):
                account.transfer(dest_id, amount)
                self.acc_repository.update(account)

            maybe_account.run(transfer_to)

        if self.transactional_context.get_errors():
            return False
        else:
            return True
