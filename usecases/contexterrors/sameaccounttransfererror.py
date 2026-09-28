from usecases.contexterrors.businesserror import BusinessError
from usecases.repositories.accountsrepositoryinterface import AccountID


class SameAccountTransferError(BusinessError):
    def __init__(self, account_id: AccountID):
        super().__init__(f"Account {account_id} cannot transfer to itself.")
