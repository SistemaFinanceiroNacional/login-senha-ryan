from drivers.web.application.bank_application import Ui
from drivers.web.application.controllers.home import HomeHandler
from drivers.web.application.controllers.logged import LoggedHandler
from drivers.web.application.controllers.logout import LogoutHandler
from drivers.web.application.controllers.register_client import (
    RegisterClientHandler
)
from drivers.web.server import main
from drivers.web.application import settings
from drivers.web.framework.template import configure_template
from drivers.web.framework.httprequest.session import (
    configure_auth_redirect,
    session_middleware
)
from infrastructure.dicontainer import DiContainer
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
        di_container = DiContainer()

        conn_pool = PostgresqlConnectionPool(max_connections=5)
        thread_id = di_container[ThreadIdentity]
        acc_repo = AccountsRepository(conn_pool, thread_id)
        clients_repo = ClientsRepository(conn_pool, thread_id)
        context = DBTransactionContext(conn_pool, thread_id)

        get_accounts = GetAccountsUseCase(acc_repo, context)
        get_balance = GetBalanceUseCase(acc_repo, context)
        get_transactions = GetTransactionsUseCase(acc_repo, context)

        register_client_use_case = RegisterClientUseCase(
            clients_repo,
            context,
            Password
        )

        auth_service = AuthServiceDB(context, conn_pool, thread_id)

        home_handler = HomeHandler(auth_service, get_accounts)
        logout_handler = di_container[LogoutHandler]
        register_handler = RegisterClientHandler(register_client_use_case)
        logged_handler = LoggedHandler(get_balance, get_transactions)

        user_interface = session_middleware(Ui(
            home_handler,
            logout_handler,
            register_handler,
            logged_handler
        ))

        configure_template(settings)
        configure_auth_redirect(settings.AUTH_REDIRECT)
        main(user_interface)
