from drivers.Cli.command_line_interface import main
from ApplicationService.connection_pool import postgresql_connection_pool
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.dbtransactioncontext import dbTransactionContext
from ApplicationService.transferFundsBetweenAccountsUseCase import transferFundsBetweenAccountsUseCase
from ApplicationService.threadIdentity import thread_identity
from ApplicationService.openAccountUseCase import openAccountUseCase
from ApplicationService.externalrepository import externalRepository
from ApplicationService.internalrepository import internalRepository
from inputIO.inputIO import inputIO


class config:
    def run_ui(self):
        conn_pool = postgresql_connection_pool()
        thread_id = thread_identity()
        int_accounts_rep = internalRepository(conn_pool, thread_id)
        exp_accounts_rep = externalRepository(conn_pool, thread_id)

        context = dbTransactionContext(conn_pool, thread_id)

        user_io = inputIO()
        login_use_case = loginUseCase(int_accounts_rep, context)
        transfer_use_case = transferFundsBetweenAccountsUseCase(int_accounts_rep, exp_accounts_rep, context)
        open_account_use_case = openAccountUseCase(int_accounts_rep, context)

        main(user_io, login_use_case, transfer_use_case, open_account_use_case)