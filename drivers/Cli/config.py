from drivers.Cli.command_line_interface import main
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.OpenAccountUseCase import OpenAccountUseCase
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.unloggedUseCases import UnloggedUseCases
from Infrastructure.dbtransactioncontext import dbTransactionContext
from Infrastructure.threadIdentity import thread_identity
from Infrastructure.accountsrepository import AccountsRepository
from Infrastructure.connection_pool import postgresql_connection_pool
from Infrastructure.authServiceDB import AuthServiceDB
from inputIO.inputIO import inputIO
from password import Password


class config:
    def run_ui(self):
        conn_pool = postgresql_connection_pool()
        thread_id = thread_identity()
        acc_rep = AccountsRepository(conn_pool, thread_id)

        context = dbTransactionContext(conn_pool, thread_id)

        user_io = inputIO()
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

        main(user_io, auth_service, unlogged_cases, logged_cases)
