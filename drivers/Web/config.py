from drivers.Web.bank_application import ui
from drivers.Web.server import main
from ApplicationService.OpenAccountUseCase import OpenAccountUseCase
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from Infrastructure.accountsrepository import AccountsRepository
from Infrastructure.connection_pool import postgresql_connection_pool
from Infrastructure.threadIdentity import thread_identity
from Infrastructure.dbtransactioncontext import dbTransactionContext
from Infrastructure.authServiceDB import AuthServiceDB
from password import Password


class config:
    def run_ui(self):
        conn_pool = postgresql_connection_pool(max_connections=5)
        thread_id = thread_identity()
        acc_rep = AccountsRepository(conn_pool, thread_id)

        context = dbTransactionContext(conn_pool, thread_id)

        transfer_use_case = TransferFundsUseCase(
            acc_rep,
            context
        )
        open_account_use_case = OpenAccountUseCase(
            acc_rep,
            context,
            Password
        )
        get_accounts_use_case = GetAccountsUseCase(acc_rep, context)
        get_balance_use_case = GetBalanceUseCase(acc_rep, context)

        auth_service = AuthServiceDB(context, conn_pool, thread_id)
        unlogged_cases = UnloggedUseCases(open_account_use_case)
        logged_cases = LoggedUseCases(
            transfer_use_case,
            get_accounts_use_case,
            get_balance_use_case
        )

        user_interface = ui(
            auth_service,
            unlogged_cases,
            logged_cases
        )

        main(user_interface)
