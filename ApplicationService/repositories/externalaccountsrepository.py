class externalAccountsRepository:
    def get_by_login(self, login: str):
        raise NotImplementedError

    def update(self, login: str, balance: float):
        raise NotImplementedError