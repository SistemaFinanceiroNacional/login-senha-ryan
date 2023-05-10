from ApplicationService.transactioncontext import transactioncontext
from ApplicationService.repositories.internalaccountsrepository import (
    internalAccountsRepository as iar
)
from ApplicationService.internal_account import internalAccount as iAccount
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

    def execute(self, internalAccount: iAccount, destLogin: str, amount):
        with self.transactional_context:
            existence = self.internalRepository.exists(destLogin)
            if not existence:
                exception = AccountDoesNotExistsError(destLogin)
                raise exception
            internalAccount.transfer(destLogin, amount)
            self.internalRepository.update_balance(internalAccount)

        if self.transactional_context.get_errors():
            return False
        else:
            return True
