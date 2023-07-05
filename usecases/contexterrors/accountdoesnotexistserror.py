from usecases.contexterrors.businesserror import BusinessError
from usecases.repositories.accountsrepositoryinterface import (
    AccountID
)


class AccountDoesNotExistsError(BusinessError):
    def __init__(self, destiny_id: AccountID):
        super().__init__(f"Account {destiny_id} does not exists.")
