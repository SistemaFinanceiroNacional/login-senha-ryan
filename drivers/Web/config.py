from drivers.Web.bankApplication import ui
from drivers.Web.server import main
from ApplicationService.openAccountUseCase import openAccountUseCase
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.transferFundsUseCase import transferFundsUseCase
from ApplicationService.accountsrepository import accountsRepository
from ApplicationService.connection_pool import postgresql_connection_pool
from ApplicationService.threadIdentity import thread_identity
from ApplicationService.dbtransactioncontext import dbTransactionContext
from password import password


class config:
    def run_ui(self):
        conn_pool = postgresql_connection_pool(max_connections=5)
        thread_id = thread_identity()
        int_acc_rep = accountsRepository(conn_pool, thread_id)

        context = dbTransactionContext(conn_pool, thread_id)

        login_use_case = loginUseCase(int_acc_rep, context, password)
        transfer_use_case = transferFundsUseCase(
            int_acc_rep,
            context
        )
        open_account_use_case = openAccountUseCase(
            int_acc_rep,
            context,
            password
        )

        user_interface = ui(
            login_use_case,
            transfer_use_case,
            open_account_use_case
        )
        main(user_interface)
