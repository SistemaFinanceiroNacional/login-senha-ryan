import maybe
from internalaccountsrepository import internalAccountsRepository
from ApplicationService.transactioncontext import transactioncontext

class loginUseCase:
    def __init__(self, account_repository: internalAccountsRepository, transactional_context: transactioncontext):
        self.account_repository = account_repository
        self.transactional_context = transactional_context

    def execute(self, username: str, password: str):
        with self.transactional_context:
            possible_account = self.account_repository.authentication(username, password)

        if self.transactional_context.get_errors():
            return maybe.nothing()

        else:
            return possible_account