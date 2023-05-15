from password import password as pw
from maybe import maybe
from ApplicationService.client import Client


class internalAccountsRepository:
    def add_account(self, login: str, password: pw) -> bool:
        raise NotImplementedError

    def authentication(self, login: str, password: pw) -> maybe[Client]:
        raise NotImplementedError

    def exists(self, destLogin: str) -> bool:
        raise NotImplementedError
