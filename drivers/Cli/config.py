import drivers.Cli.command_line_interface as cli
import ApplicationService.connection_pool as cpool
import ApplicationService.loginUseCase as lCase
import ApplicationService.dbtransactioncontext as ctxt
import ApplicationService.transferFundsBetweenAccountsUseCase as tfba
import ApplicationService.identity as identifier
import ApplicationService.openAccountUseCase as open_acc
from ApplicationService import externalrepository as eai, internalrepository as iar
import inputIO.inputIO as io

class config:
    def run_ui(self):
        conn_pool = cpool.postgresql_connection_pool()
        thread_id = identifier.thread_identity()
        accounts_rep = iar.internalRepository(conn_pool, thread_id)
        exp_accounts_rep = eai.externalRepository(conn_pool, thread_id)
        context = ctxt.dbTransactionContext(conn_pool, thread_id)

        user_io = io.inputIO()
        login_use_case = lCase.loginUseCase(accounts_rep, context)
        transfer_use_case = tfba.transferFundsBetweenAccountsUseCase(accounts_rep, exp_accounts_rep, context)
        open_account_use_case = open_acc.openAccountUseCase(accounts_rep, context)

        cli.main(user_io, login_use_case, transfer_use_case, open_account_use_case)