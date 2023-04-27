from maybe import maybe
from ApplicationService.external_account import externalAccount


class externalAccountsRepository:
    def get_by_login(self, login: str) -> maybe[externalAccount]:
        raise NotImplementedError

    def update(self, extAccount: externalAccount) -> None:
        raise NotImplementedError
