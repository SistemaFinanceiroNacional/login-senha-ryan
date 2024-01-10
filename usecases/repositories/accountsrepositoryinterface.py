from typing import Iterable
from domain.bankaccount import (
    BankAccount,
)
from domain.commontypes.types import (
    ClientId,
    AccountId
)
from maybe import Maybe


class AccountsRepositoryInterface:
    def add_account(self, client_id: ClientId) -> bool:
        raise NotImplementedError

    def exists(self, account_id: AccountId) -> bool:
        raise NotImplementedError

    def update(self, account: BankAccount) -> None:
        raise NotImplementedError

    def get_by_client_id(self, client_id: ClientId) -> Iterable[AccountId]:
        raise NotImplementedError

    def get_by_id(self, account_id: AccountId) -> Maybe[BankAccount]:
        raise NotImplementedError
