from typing import List
from password import password as pw
from ApplicationService.account import Account


class Client:
    def __init__(self,
                 login: str,
                 password: pw,
                 accounts: List[Account]
                 ):
        self._login = login
        self._password = password
        self._accounts = accounts

    def get_accounts(self):
        return self._accounts
