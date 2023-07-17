from drivers.web.application.bank_application import Ui
from drivers.web.server import main
from drivers.web.application import settings
from drivers.web.framework.template import configure_template
from drivers.web.framework.httprequest.session import configure_auth_redirect, session_middleware
from usecases.new_bank_account import NewBankAccountUseCase
from usecases.transfer import TransferFundsUseCase
from usecases.unlogged_cases import UnloggedUseCases
from usecases.logged_cases import LoggedUseCases
from usecases.get_accounts import GetAccountsUseCase
from usecases.get_balance import GetBalanceUseCase
from usecases.register_client import RegisterClientUseCase
from usecases.get_transactions import GetTransactionsUseCase
from infrastructure.accountsrepository import AccountsRepository
from infrastructure.clientsrepository import ClientsRepository
from infrastructure.connection_pool import PostgresqlConnectionPool
from infrastructure.threadIdentity import ThreadIdentity
from infrastructure.dbtransactioncontext import DBTransactionContext
from infrastructure.authservicedb import AuthServiceDB
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

        user_interface = session_middleware(Ui(
            auth_service,
            unlogged_cases,
            logged_cases
        ))

        configure_template(settings)
        configure_auth_redirect(settings.AUTH_REDIRECT)
        main(user_interface)
