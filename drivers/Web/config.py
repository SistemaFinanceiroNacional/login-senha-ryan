from drivers.Web.bank_application import Ui
from drivers.Web.server import main
from ApplicationService.newbankaccountusecase import NewBankAccountUseCase
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from ApplicationService.registerclientusecase import RegisterClientUseCase
from ApplicationService.gettransactionsusecase import GetTransactionsUseCase
from Infrastructure.accountsrepository import AccountsRepository
from Infrastructure.clientsrepository import ClientsRepository
from Infrastructure.connection_pool import PostgresqlConnectionPool
from Infrastructure.threadIdentity import ThreadIdentity
from Infrastructure.dbtransactioncontext import DBTransactionContext
from Infrastructure.authServiceDB import AuthServiceDB
from password import Password


class Config:
    def run_ui(self):
        conn_pool = PostgresqlConnectionPool(max_connections=5)
        thread_id = ThreadIdentity()
        acc_repo = AccountsRepository(conn_pool, thread_id)
        clients_repo = ClientsRepository(conn_pool, thread_id)
        context = DBTransactionContext(conn_pool, thread_id)

        transfer_use_case = TransferFundsUseCase(acc_repo, context)
        get_accounts_use_case = GetAccountsUseCase(acc_repo, context)
        get_balance_use_case = GetBalanceUseCase(acc_repo, context)
        get_transactions_use_case = GetTransactionsUseCase(acc_repo, context)
        new_bank_account_use_case = NewBankAccountUseCase(acc_repo, context)

        logged_cases = LoggedUseCases(
            transfer_use_case,
            get_accounts_use_case,
            get_balance_use_case,
            get_transactions_use_case,
            new_bank_account_use_case
        )

        register_client_use_case = RegisterClientUseCase(
            clients_repo,
            context,
            Password
        )

        auth_service = AuthServiceDB(context, conn_pool, thread_id)
        unlogged_cases = UnloggedUseCases(register_client_use_case)

        user_interface = Ui(
            auth_service,
            unlogged_cases,
            logged_cases
        )

        main(user_interface)
