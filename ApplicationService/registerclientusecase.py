from typing import Callable
from ApplicationService.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface as c_repo
)
from ApplicationService.repositories.transactioncontext import (
    transactioncontext as cntx
)
from password import Password


PasswordMaker = Callable[[str], Password]


class RegisterClientUseCase:
    def __init__(self,
                 clients_repository: c_repo,
                 trans_context: cntx,
                 pw_maker: PasswordMaker
                 ):
        self.clients_repository = clients_repository
        self.transactional_context = trans_context
        self.pw_maker = pw_maker

    def execute(self, login: str, pw: str) -> bool:
        if not login or not pw:
            return False
        made_pw = self.pw_maker(pw)
        with self.transactional_context:
            ret = self.clients_repository.add_client(login, made_pw)

        if self.transactional_context.get_errors():
            return False
        else:
            return ret
