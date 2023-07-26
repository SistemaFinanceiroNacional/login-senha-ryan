from drivers.web.application.bank_application import Ui
from drivers.web.application import settings
from drivers.web.server import main
from drivers.web.framework.template import configure_template
from drivers.web.framework.httprequest.session import (
    configure_auth_redirect,
    session_middleware
)
from infrastructure.authserviceinterface import AuthServiceInterface
from infrastructure.connectionInterface import ConnectionPool
from infrastructure.dicontainer import DiContainer
from infrastructure.identityinterface import IdentityInterface
from infrastructure.accountsrepository import AccountsRepository
from infrastructure.clientsrepository import ClientsRepository
from infrastructure.connection_pool import (
    PostgresqlConnectionPool,
    psycopg2_create_connection, ConnMaker
)
from infrastructure.threadIdentity import ThreadIdentity
from infrastructure.dbtransactioncontext import DBTransactionContext
from infrastructure.authservicedb import AuthServiceDB
from usecases.register_client import PasswordMaker
from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface
)
from usecases.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)
from password import Password


class Config:
    def run_ui(self):
        di_container = DiContainer()

        di_container[ConnMaker] = psycopg2_create_connection
        di_container[PasswordMaker] = Password

        di_container.set_parameter('max_connections', 1)

        di_container.provide(ConnectionPool, PostgresqlConnectionPool)
        di_container.provide(IdentityInterface, ThreadIdentity)
        di_container.provide(TransactionContextInterface, DBTransactionContext)
        di_container.provide(AccountsRepositoryInterface, AccountsRepository)
        di_container.provide(ClientsRepositoryInterface, ClientsRepository)
        di_container.provide(AuthServiceInterface, AuthServiceDB)

        user_interface = session_middleware(di_container[Ui])

        configure_template(settings)
        configure_auth_redirect(settings.AUTH_REDIRECT)
        main(user_interface)
