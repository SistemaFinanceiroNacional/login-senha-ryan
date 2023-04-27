from password import password as pw
from maybe import maybe
from ApplicationService.internal_account\
    import internalAccount as ia


class internalAccountsRepository:
    def add_account(self, login: str, password: pw) -> bool:
        raise NotImplementedError

    def authentication(self, login: str, password: pw) -> maybe[ia]:
        raise NotImplementedError

    def update_balance(self, intAccount: ia) -> None:
        raise NotImplementedError
