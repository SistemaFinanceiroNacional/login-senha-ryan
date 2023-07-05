from typing import Callable
from usecases.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface as CRepo
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)
from password import Password


PasswordMaker = Callable[[str], Password]


class RegisterClientUseCase:
    def __init__(self,
                 clients_repository: CRepo,
                 trans_context: Cntx,
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
