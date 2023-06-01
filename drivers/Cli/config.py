from drivers.Cli.command_line_interface import main
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.newbankaccountusecase import NewBankAccountUseCase
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.registerclientusecase import RegisterClientUseCase
from ApplicationService.gettransactionsusecase import GetTransactionsUseCase
from Infrastructure.dbtransactioncontext import dbTransactionContext
from Infrastructure.threadIdentity import thread_identity
from Infrastructure.accountsrepository import AccountsRepository
from Infrastructure.clientsrepository import ClientsRepository
from Infrastructure.connection_pool import postgresql_connection_pool
from Infrastructure.authServiceDB import AuthServiceDB
from inputIO.inputIO import inputIO
from password import Password


class config:
    def run_ui(self):
        conn_pool = postgresql_connection_pool()
        thread_id = thread_identity()
        acc_repo = AccountsRepository(conn_pool, thread_id)
        clients_repo = ClientsRepository(conn_pool, thread_id)
        context = dbTransactionContext(conn_pool, thread_id)
        user_io = inputIO()

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

        main(user_io, auth_service, unlogged_cases, logged_cases)
