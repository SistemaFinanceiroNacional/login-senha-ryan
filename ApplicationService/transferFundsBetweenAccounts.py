
class transferFundsBetweenAccountsClass:
    def __init__(self, internalRepository, externalRepository):
        self.internalRepository = internalRepository
        self.externalRepository = externalRepository

    def execute(self, internalAccount, destinyLogin, amount):
        extAccount = self.externalRepository.getByLogin(destinyLogin).orElseThrow(accountDoesNotExists(destinyLogin))
        internalAccount.transfer(extAccount, amount)
        internalAccount.update(self.internalRepository)
        extAccount.update(self.externalRepository)


class accountDoesNotExists(Exception):
    def __init__(self,destinyLogin):
        self.destinyLogin = destinyLogin
        super().__init__(f"{destinyLogin} does not exists as a login.")
