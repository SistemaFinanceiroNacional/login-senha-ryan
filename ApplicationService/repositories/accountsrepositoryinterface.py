from password import password as pw
from maybe import maybe


accountID = int

class AccountsRepositoryInterface:
    def add_account(self, login: str, password: pw) -> bool:
        raise NotImplementedError

    def exists(self, destLogin: str) -> bool:
        raise NotImplementedError

    def update(self, account):
        raise NotImplementedError

    def get_account_id(self, client_login: str) -> accountID:
        raise NotImplementedError