from ApplicationService.transactioncontext import transactioncontext
from ApplicationService.repositories.internalaccountsrepository import (
    internalAccountsRepository as iar
)
from ApplicationService.repositories.externalaccountsrepository import (
    externalAccountsRepository as exar
)
from ApplicationService.internal_account import internalAccount as iAccount
from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)


class transferFundsUseCase:
    def __init__(self,
                 internalRepository: iar,
                 externalRepository: exar,
                 transactional_context: transactioncontext
                 ):
        self.internalRepository = internalRepository
        self.externalRepository = externalRepository
        self.transactional_context = transactional_context

    def execute(self, internalAccount: iAccount, destinyLogin: str, amount):
        with self.transactional_context:
            extAccount = self.externalRepository.get_by_login(destinyLogin).\
                orElseThrow(AccountDoesNotExistsError(destinyLogin))
            internalAccount.transfer(extAccount, amount)
            self.internalRepository.update_balance(internalAccount)
            self.externalRepository.update(extAccount)

        if self.transactional_context.get_errors():
            return False
        else:
            return True
