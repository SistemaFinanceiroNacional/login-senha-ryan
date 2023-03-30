from ApplicationService.repositories.internalaccountsrepository import internalAccountsRepository
from ApplicationService.transactioncontext import transactioncontext

class openAccountUseCase:
    def __init__(self, accounts_repository: internalAccountsRepository, transactional_context: transactioncontext):
        self.accounts_repository = accounts_repository
        self.transactional_context = transactional_context

    def execute(self, login: str, password: str) -> bool:
        with self.transactional_context:
            ret = self.accounts_repository.add_account(login, password)

        if self.transactional_context.get_errors():
            return False
        else:
            return ret