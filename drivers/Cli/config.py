from drivers.Cli.command_line_interface import main
from ApplicationService.connection_pool import postgresql_connection_pool
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.dbtransactioncontext import dbTransactionContext
from ApplicationService.transferFundsUseCase import transferFundsUseCase
from ApplicationService.threadIdentity import thread_identity
from ApplicationService.openAccountUseCase import openAccountUseCase
from ApplicationService.externalrepository import externalRepository
from ApplicationService.internalrepository import internalRepository
from inputIO.inputIO import inputIO
from password import password as pw


class config:
    def run_ui(self):
        conn_pool = postgresql_connection_pool()
        thread_id = thread_identity()
        int_acc_rep = internalRepository(conn_pool, thread_id)
        exp_acc_rep = externalRepository(conn_pool, thread_id)

        context = dbTransactionContext(conn_pool, thread_id)

        user_io = inputIO()
        login_use_case = loginUseCase(int_acc_rep, context, pw)
        transfer_use_case = transferFundsUseCase(
            int_acc_rep,
            exp_acc_rep,
            context
        )
        open_account_use_case = openAccountUseCase(int_acc_rep, context, pw)

        main(user_io, login_use_case, transfer_use_case, open_account_use_case)
