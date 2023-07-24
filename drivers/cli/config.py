from drivers.cli.command_line_interface import main
from usecases.transfer import TransferFundsUseCase
from usecases.new_bank_account import NewBankAccountUseCase
from usecases.get_accounts import GetAccountsUseCase
from usecases.get_balance import GetBalanceUseCase
from usecases.logged_cases import LoggedUseCases
from usecases.unlogged_cases import UnloggedUseCases
from usecases.register_client import RegisterClientUseCase
from usecases.get_transactions import GetTransactionsUseCase
from infrastructure.dbtransactioncontext import DBTransactionContext
from infrastructure.threadIdentity import ThreadIdentity
from infrastructure.accountsrepository import AccountsRepository
from infrastructure.clientsrepository import ClientsRepository
from infrastructure.connection_pool import (
    PostgresqlConnectionPool,
    psycopg2_create_connection
)
from infrastructure.authservicedb import AuthServiceDB
from inputio.input_io import InputIO
from password import Password


class Config:
    def run_ui(self):
        conn_pool = PostgresqlConnectionPool(psycopg2_create_connection, 1)
        thread_id = ThreadIdentity()
        acc_repo = AccountsRepository(conn_pool, thread_id)
        clients_repo = ClientsRepository(conn_pool, thread_id)
        context = DBTransactionContext(conn_pool, thread_id)
        user_io = InputIO()

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
