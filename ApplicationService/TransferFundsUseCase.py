from ApplicationService.repositories.transactioncontext import (
    transactioncontext
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
                 transactional_context: transactioncontext
                 ):
        self.acc_repository = acc_repository
        self.transactional_context = transactional_context

    def execute(self, acc_id: AccountID, destID: int, amount):
        with self.transactional_context:
            existence = self.acc_repository.exists(destID)
            if not existence:
                exception = AccountDoesNotExistsError(str(destID))
                raise exception
            account = self.acc_repository.get_by_id(acc_id)
            account.transfer(destID, amount)
            self.acc_repository.update(account)
        if self.transactional_context.get_errors():
            return False
        else:
            return True
