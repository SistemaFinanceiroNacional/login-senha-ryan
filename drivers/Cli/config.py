import drivers.Cli.command_line_interface as cli
import ApplicationService.connection_pool as cpool
import ApplicationService.loginUseCase as lcase

class config:
    def run_ui(self):
        conn_pool = cpool.postgresql_connection_pool()
        accounts_rep = lcase.login_use_case()

        cli.main()