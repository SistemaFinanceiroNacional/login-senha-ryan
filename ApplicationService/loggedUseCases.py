from ApplicationService.TransferFundsUseCase import (
    TransferFundsUseCase as tfuc
)
from ApplicationService.getAccountsUseCase import (
    GetAccountsUseCase as gauc
)
from ApplicationService.getBalanceUseCase import (
    GetBalanceUseCase as gbuc
)
from ApplicationService.gettransactionsusecase import (
    GetTransactionsUseCase as gtuc
)
from ApplicationService.newbankaccountusecase import (
    NewBankAccountUseCase as nbauc
)


class LoggedUseCases:
    def __init__(self,
                 transfer: tfuc,
                 get_accounts: gauc,
                 get_balance: gbuc,
                 get_transactions: gtuc,
                 new_bank_account: nbauc
                 ):
        self.transfer = transfer
        self.get_accounts = get_accounts
        self.get_balance = get_balance
        self.get_transactions = get_transactions
        self.new_bank_account: new_bank_account
