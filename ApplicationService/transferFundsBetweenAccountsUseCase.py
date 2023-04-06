from ApplicationService.transactioncontext import transactioncontext
from ApplicationService.repositories.internalaccountsrepository import internalAccountsRepository
from ApplicationService.repositories.externalaccountsrepository import externalAccountsRepository
from ApplicationService.internalAccount import internalAccount as iAccount
from ApplicationService.contexterrors.accountdoesnotexistserror import AccountDoesNotExistsError

class transferFundsBetweenAccountsUseCase:
    def __init__(self, internalRepository: internalAccountsRepository, externalRepository: externalAccountsRepository, transactional_context: transactioncontext):
        self.internalRepository = internalRepository
        self.externalRepository = externalRepository
        self.transactional_context = transactional_context

    def execute(self, internalAccount: iAccount, destinyLogin: str, amount):
        with self.transactional_context:
            extAccount = self.externalRepository.get_by_login(destinyLogin).orElseThrow(AccountDoesNotExistsError(destinyLogin))
            internalAccount.transfer(extAccount, amount)
            internalAccount.update(self.internalRepository)
            extAccount.update(self.externalRepository)

        if self.transactional_context.get_errors():
            return False
        else:
            return True
