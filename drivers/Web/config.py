from drivers.Web.bankApplication import ui
from drivers.Web.server import main
from ApplicationService.openAccountUseCase import openAccountUseCase
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.transferFundsUseCase import transferFundsUseCase
from ApplicationService.internalrepository import internalRepository
from ApplicationService.externalrepository import externalRepository
from ApplicationService.connection_pool import postgresql_connection_pool
from ApplicationService.threadIdentity import thread_identity
from ApplicationService.dbtransactioncontext import dbTransactionContext


class config:
    def run_ui(self):
        conn_pool = postgresql_connection_pool(max_connections=5)
        thread_id = thread_identity()
        int_accounts_rep = internalRepository(conn_pool, thread_id)
        ext_accounts_rep = externalRepository(conn_pool, thread_id)

        context = dbTransactionContext(conn_pool, thread_id)

        login_use_case = loginUseCase(int_accounts_rep, context)
        transfer_use_case = transferFundsUseCase(
            int_accounts_rep,
            ext_accounts_rep,
            context
        )
        open_account_use_case = openAccountUseCase(int_accounts_rep, context)

        user_interface = ui(
            login_use_case,
            transfer_use_case,
            open_account_use_case
        )
        main(user_interface)
