from ApplicationService.repositories.transactioncontext import transactioncontext
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as repo
)
from Domain.account import Account as acc
from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)


class TransferFundsUseCase:
    def __init__(self,
                 internalRepository: repo,
                 transactional_context: transactioncontext
                 ):
        self.internalRepository = internalRepository
        self.transactional_context = transactional_context

    def execute(self, account: acc, destID: int, amount):
        with self.transactional_context:
            existence = self.internalRepository.exists(destID)
            if not existence:
                exception = AccountDoesNotExistsError(destID)
                raise exception
            account.transfer(destID, amount)
            self.internalRepository.update(account)
        if self.transactional_context.get_errors():
            return False
        else:
            return True
