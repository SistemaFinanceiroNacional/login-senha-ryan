from drivers.Web.bank_application import ui
from drivers.Web.server import main
from ApplicationService.OpenAccountUseCase import OpenAccountUseCase
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from Infrastructure.accountsrepository import AccountsRepository
from Infrastructure.connection_pool import postgresql_connection_pool
from Infrastructure.threadIdentity import thread_identity
from Infrastructure.dbtransactioncontext import dbTransactionContext
from password import Password


class config:
    def run_ui(self):
        conn_pool = postgresql_connection_pool(max_connections=5)
        thread_id = thread_identity()
        int_acc_rep = AccountsRepository(conn_pool, thread_id)

        context = dbTransactionContext(conn_pool, thread_id)

        login_use_case = loginUseCase(int_acc_rep, context, Password)
        transfer_use_case = TransferFundsUseCase(
            int_acc_rep,
            context
        )
        open_account_use_case = OpenAccountUseCase(
            int_acc_rep,
            context,
            Password
        )

        user_interface = ui(
            login_use_case,
            transfer_use_case,
            open_account_use_case
        )
        main(user_interface)
