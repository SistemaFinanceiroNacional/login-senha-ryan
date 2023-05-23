from typing import Callable
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as repo
)
from ApplicationService.repositories.transactioncontext import (
    transactioncontext as cntx
)
from password import Password


PasswordMaker = Callable[[str], Password]


class OpenAccountUseCase:
    def __init__(self,
                 acc_repository: repo,
                 trans_context: cntx,
                 pw_maker: PasswordMaker
                 ):
        self.accounts_repository = acc_repository
        self.transactional_context = trans_context
        self.pw_maker = pw_maker

    def execute(self, login: str, pw: str) -> bool:
        if not login or not pw:
            return False
        made_pw = self.pw_maker(pw)
        with self.transactional_context:
            ret = self.accounts_repository.add_account(login, made_pw)

        if self.transactional_context.get_errors():
            return False
        else:
            return ret
