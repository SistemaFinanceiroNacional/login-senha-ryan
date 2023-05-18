from ApplicationService.contexterrors.businesserror import BusinessError


class AccountDoesNotExistsError(BusinessError):
    def __init__(self, destinyID: str):
        self.destinyID = destinyID
        super().__init__(f"{destinyID} does not exists as a login.")
