from typing import Iterable
from password import Password as pw
from Domain.account import Account

ClientID = int
AccountID = int
Balance = float


class AccountsRepositoryInterface:
    def add_client(self, login: str, password: pw) -> bool:
        raise NotImplementedError

    # def add_account(self, client_id: ClientID) -> bool:
    #     raise NotImplementedError

    def exists(self, destID: int) -> bool:
        raise NotImplementedError

    def update(self, account: Account) -> None:
        raise NotImplementedError

    def get_by_client_id(self, client_id: ClientID) -> Iterable[AccountID]:
        raise NotImplementedError

    def get_by_id(self, account_id: AccountID) -> Account:
        raise NotImplementedError

    def get_balance(self, account_id: AccountID) -> Balance:
        raise NotImplementedError