from typing import Iterable
from Domain.account import (
    Account,
)
from Domain.CommonTypes.types import (
    ClientID,
    AccountID
)
from maybe import Maybe


class AccountsRepositoryInterface:
    def add_account(self, client_id: ClientID) -> bool:
        raise NotImplementedError

    def exists(self, account_id: AccountID) -> bool:
        raise NotImplementedError

    def update(self, account: Account) -> None:
        raise NotImplementedError

    def get_by_client_id(self, client_id: ClientID) -> Iterable[AccountID]:
        raise NotImplementedError

    def get_by_id(self, account_id: AccountID) -> Maybe[Account]:
        raise NotImplementedError
