from typing import Callable
from maybe import maybe, nothing
from ApplicationService.transactioncontext import (
    transactioncontext as cntx
)
from ApplicationService.clientsrepository import ClientsRepository as cr
from password import password


PasswordMaker = Callable[[str], password]
clientLogin = str


class loginUseCase:
    def __init__(self,
                 c_repository: cr,
                 transactional_context: cntx,
                 pw_maker: PasswordMaker
                 ):
        self.clients_repository = c_repository
        self.transactional_context = transactional_context
        self.pw_maker = pw_maker

    def execute(self, login: str, pw: str) -> maybe[clientLogin]:
        if not login or not pw:
            return nothing()
        made_pw = self.pw_maker(pw)
        with self.transactional_context:
            possible_client = self.clients_repository.get_by_credentials(login, made_pw)

        if self.transactional_context.get_errors():
            return nothing()
        else:
            return possible_client.map(lambda client: client.get_login())
