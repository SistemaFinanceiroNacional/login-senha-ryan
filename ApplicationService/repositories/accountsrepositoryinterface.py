from typing import Iterable

from password import Password as pw


AccountID = int
Balance = float


class AccountsRepositoryInterface:
    def add_account(self, login: str, password: pw) -> bool:
        raise NotImplementedError

    def exists(self, destID: int) -> bool:
        raise NotImplementedError

    def update(self, account):
        raise NotImplementedError

    def get_by_client_id(self, client_id: int) -> Iterable[AccountID]:
        raise NotImplementedError

    def get_balance(self, account_id: AccountID) -> Balance:
        raise NotImplementedError