from datetime import timedelta

from drivers.web.framework.httprequest.sessionstore import (
    SessionStoreInterface
)
from infrastructure.connection_pool import ConnectionPool as CPool
from infrastructure.identityinterface import IdentityInterface
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)


class DBSessionStore(SessionStoreInterface):
    """Sessions in PostgreSQL. A session ends after `idle_timeout` without
    requests or `lifetime` after it started, whichever comes first."""

    def __init__(self,
                 context: TransactionContextInterface,
                 connection_pool: CPool,
                 identifier: IdentityInterface,
                 idle_timeout: timedelta,
                 lifetime: timedelta
                 ):
        self.context = context
        self.connection_pool = connection_pool
        self.identifier = identifier
        self.idle_timeout = idle_timeout
        self.lifetime = lifetime
