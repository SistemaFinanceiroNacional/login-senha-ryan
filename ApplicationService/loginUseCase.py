import maybe
from ApplicationService.repositories.internalaccountsrepository import internalAccountsRepository
from ApplicationService.transactioncontext import transactioncontext
from password import password as pw
import logging

logger = logging.getLogger("ApplicationService.loginUseCase")

class loginUseCase:
    def __init__(self, account_repository: internalAccountsRepository, transactional_context: transactioncontext):
        self.account_repository = account_repository
        self.transactional_context = transactional_context

    def execute(self, username: str, password: pw):
        with self.transactional_context:
            possible_account = self.account_repository.authentication(username, password)

        if self.transactional_context.get_errors():
            return maybe.nothing()

        else:
            return possible_account