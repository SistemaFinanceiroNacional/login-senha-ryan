from ApplicationService.contexterrors.businesserror import BusinessError

class AccountDoesNotExistsError(BusinessError):
    def __init__(self, destinyLogin):
        self.destinyLogin = destinyLogin
        super().__init__(f"{destinyLogin} does not exists as a login.")