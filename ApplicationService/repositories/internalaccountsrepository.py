from password import password as pw
from maybe import maybe
from ApplicationService.internal_account import internalAccount

class internalAccountsRepository:
    def add_account(self, login: str, password: pw) -> bool:
        raise NotImplementedError

    def authentication(self, login: str, password: pw) -> maybe[internalAccount]:
        raise NotImplementedError

    def update_balance(self, intAccount: internalAccount) -> None:
        raise NotImplementedError