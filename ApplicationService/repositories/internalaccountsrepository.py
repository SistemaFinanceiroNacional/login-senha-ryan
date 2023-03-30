
class internalAccountsRepository:
    def add_account(self, login: str, password: str):
        raise NotImplementedError

    def authentication(self, login: str, password: str):
        raise NotImplementedError

    def update_balance(self, login: str, balance: float):
        raise NotImplementedError