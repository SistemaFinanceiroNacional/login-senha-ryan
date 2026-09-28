from datetime import timedelta
from os import getenv

from drivers.web.application.entrypoint import get_application
from drivers.web.application.sessionstore import DBSessionStore
from drivers.web.framework.httprequest.sessionstore import (
    SessionStoreInterface
)
from drivers.web.server import main
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
from infrastructure.ceremoniesrepository import CeremoniesRepository
from infrastructure.passkeysrepository import PasskeysRepository
from infrastructure.webauthnrelyingparty import WebAuthnRelyingParty
from usecases.passkeys.relyingpartyinterface import RelyingPartyInterface
from usecases.repositories.ceremoniesrepositoryinterface import (
    CeremoniesRepositoryInterface
)
from usecases.repositories.passkeysrepositoryinterface import (
    PasskeysRepositoryInterface
)
from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface
)
from usecases.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)


class Config:
    def run_ui(self):
        di_container = DiContainer()

        di_container[ConnMaker] = psycopg2_create_connection

        di_container.set_parameter('max_connections', 1)
        di_container.set_parameter('idle_timeout', timedelta(minutes=30))
        di_container.set_parameter('lifetime', timedelta(hours=12))
        di_container.set_parameter(
            'rp_id', getenv("WEBAUTHN_RP_ID", "localhost")
        )
        di_container.set_parameter('rp_name', "Sistema Financeiro Nacional")
        di_container.set_parameter(
            'origin', getenv("WEBAUTHN_ORIGIN", "http://localhost:8080")
        )

        di_container.provide(ConnectionPool, PostgresqlConnectionPool)
        di_container.provide(IdentityInterface, ThreadIdentity)
        di_container.provide(TransactionContextInterface, DBTransactionContext)
        di_container.provide(AccountsRepositoryInterface, AccountsRepository)
        di_container.provide(ClientsRepositoryInterface, ClientsRepository)
        di_container.provide(PasskeysRepositoryInterface, PasskeysRepository)
        di_container.provide(
            CeremoniesRepositoryInterface, CeremoniesRepository
        )
        di_container.provide(RelyingPartyInterface, WebAuthnRelyingParty)
        di_container.provide(SessionStoreInterface, DBSessionStore)

        user_interface = get_application(di_container)
        main(user_interface)
