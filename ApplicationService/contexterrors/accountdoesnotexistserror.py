from ApplicationService.contexterrors.businesserror import BusinessError
from ApplicationService.repositories.accountsrepositoryinterface import (
    AccountID
)

class AccountDoesNotExistsError(BusinessError):
    def __init__(self, destinyID: AccountID):
        super().__init__(f"{destinyID} does not exists as a login.")
