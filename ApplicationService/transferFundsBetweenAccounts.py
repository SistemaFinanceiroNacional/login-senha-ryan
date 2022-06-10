import accounts
import externalAccountsInteractions

class transferFundsBetweenAccountsClass:
    def __init__(self, internalRepository, externalRepository):
        self.internalRepository = internalRepository
        self.externalRepository = externalRepository

<<<<<<< HEAD
    def execute(self, internalAccount, destinyLogin, amount):
        extAccount = self.externalRepository.getByLogin(destinyLogin).orElseThrow(accountDoesNotExists(destinyLogin))
        internalAccount.transfer(extAccount, amount)
        internalAccount.update(self.internalRepository)
        extAccount.update(self.externalRepository)


=======
    def execute(self,internalAccount,destinyLogin,amount):
        extAccount = self.externalRepository.getByLogin(destinyLogin).orElseThrow(accountDoesNotExists(destinyLogin))
        internalAccount.transfer(extAccount,amount)
        internalAccount.update(self.internalRepository)
        extAccount.update(self.externalRepository)

>>>>>>> The transfer on transferFundsBetweenAccounts now can receive a destinyLogin and transform it into an externalAccount. We also initiated our web implementation.
class accountDoesNotExists(Exception):
    def __init__(self,destinyLogin):
        self.destinyLogin = destinyLogin
        super().__init__(f"{destinyLogin} does not exists as a login.")
