from maybe import maybe, nothing
from ApplicationService.repositories.internalaccountsrepository\
    import internalAccountsRepository as iar
from ApplicationService.transactioncontext \
    import transactioncontext as cntx
from ApplicationService.internal_account import internalAccount
from password import password as pw
import logging

logger = logging.getLogger("ApplicationService.loginUseCase")


class loginUseCase:
    def __init__(self, account_repository: iar, transactional_context: cntx):
        self.account_repository = account_repository
        self.transactional_context = transactional_context

    def execute(self, username: str, password: pw) -> maybe[internalAccount]:
        with self.transactional_context:
            possible_account = self.account_repository.authentication(
                username, password
            )

        if self.transactional_context.get_errors():
            return nothing()

        else:
            return possible_account
