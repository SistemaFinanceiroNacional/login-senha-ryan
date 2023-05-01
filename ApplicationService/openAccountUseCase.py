from ApplicationService.repositories.internalaccountsrepository import (
    internalAccountsRepository as iar
)
from ApplicationService.transactioncontext import (
    transactioncontext as cntx
)
from password import password as pw


class openAccountUseCase:
    def __init__(self, accounts_repository: iar, transactional_context: cntx):
        self.accounts_repository = accounts_repository
        self.transactional_context = transactional_context

    def execute(self, login: str, password: pw) -> bool:
        with self.transactional_context:
            ret = self.accounts_repository.add_account(login, password)

        if self.transactional_context.get_errors():
            return False
        else:
            return ret
