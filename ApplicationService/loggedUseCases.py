from ApplicationService.TransferFundsUseCase import (
    TransferFundsUseCase as tfuc
)
from ApplicationService.getAccountsUseCase import GetAccountsUseCase as gauc
from ApplicationService.getBalanceUseCase import GetBalanceUseCase as gbuc


class LoggedUseCases:
    def __init__(self,
                 transfer: tfuc,
                 get_accounts: gauc,
                 get_balance: gbuc
                 ):
        self.transfer_use_case = transfer
        self.get_accounts_use_case = get_accounts
        self.get_balance_use_case = get_balance