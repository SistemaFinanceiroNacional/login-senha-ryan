from ApplicationService.repositories.transactioncontextinterface import (
    TransactionContextInterface as t_cntx
)
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as a_repo,
    AccountID
)
from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)


class TransferFundsUseCase:
    def __init__(self,
                 acc_repository: a_repo,
                 transactional_context: t_cntx
                 ):
        self.acc_repository = acc_repository
        self.transactional_context = transactional_context

    def execute(self,
                acc_id: AccountID,
                dest_id: AccountID,
                amount: float
                ) -> bool:
        with self.transactional_context:
            existence = self.acc_repository.exists(dest_id)
            if not existence:
                exception = AccountDoesNotExistsError(dest_id)
                raise exception
            account = self.acc_repository.get_by_id(acc_id)
            account.transfer(dest_id, amount)
            self.acc_repository.update(account)
        if self.transactional_context.get_errors():
            return False
        else:
            return True
