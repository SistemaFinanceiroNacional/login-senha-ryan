from usecases.transfer import (
    TransferFundsUseCase as TransferCase
)
from usecases.get_accounts import (
    GetAccountsUseCase as GetAccsCase
)
from usecases.get_balance import (
    GetBalanceUseCase as BalanceCase
)
from usecases.get_transactions import (
    GetTransactionsUseCase as TransactionsCase
)
from usecases.new_bank_account import (
    NewBankAccountUseCase as NewBankAccCase
)


class LoggedUseCases:
    def __init__(self,
                 transfer: TransferCase,
                 get_accounts: GetAccsCase,
                 get_balance: BalanceCase,
                 get_transactions: TransactionsCase,
                 new_bank_account: NewBankAccCase
                 ):
        self.transfer = transfer
        self.get_accounts = get_accounts
        self.get_balance = get_balance
        self.get_transactions = get_transactions
        self.new_bank_account = new_bank_account
