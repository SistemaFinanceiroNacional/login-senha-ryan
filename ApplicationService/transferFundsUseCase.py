from ApplicationService.transactioncontext import transactioncontext
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as iar
)
from ApplicationService.account import Account as acc
from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)


class transferFundsUseCase:
    def __init__(self,
                 internalRepository: iar,
                 transactional_context: transactioncontext
                 ):
        self.internalRepository = internalRepository
        self.transactional_context = transactional_context

    def execute(self, account: acc, destLogin: str, amount):
        with self.transactional_context:
            existence = self.internalRepository.exists(destLogin)
            if not existence:
                exception = AccountDoesNotExistsError(destLogin)
                raise exception
            account.transfer(destLogin, amount)
            self.internalRepository.update(account)
        if self.transactional_context.get_errors():
            return False
        else:
            return True
