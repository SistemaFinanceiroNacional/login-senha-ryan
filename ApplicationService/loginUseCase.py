from typing import Callable
from maybe import maybe, nothing
from ApplicationService.repositories.internalaccountsrepository import (
    internalAccountsRepository as iar
)
from ApplicationService.transactioncontext import (
    transactioncontext as cntx
)
from ApplicationService.client import Client
from password import password


PasswordMaker = Callable[[str], password]


class loginUseCase:
    def __init__(self,
                 account_repository: iar,
                 transactional_context: cntx,
                 pw_maker: PasswordMaker
                 ):
        self.acc_repository = account_repository
        self.transactional_context = transactional_context
        self.pw_maker = pw_maker

    def execute(self, login: str, pw: str) -> maybe[Client]:
        if not login or not pw:
            return nothing()
        made_pw = self.pw_maker(pw)
        with self.transactional_context:
            possible_acc = self.acc_repository.authentication(login, made_pw)

        if self.transactional_context.get_errors():
            return nothing()
        else:
            return possible_acc
