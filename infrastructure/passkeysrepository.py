from infrastructure.connection_pool import ConnectionPool as CPool
from infrastructure.identityinterface import IdentityInterface
from usecases.repositories.passkeysrepositoryinterface import (
    PasskeysRepositoryInterface
)


class PasskeysRepository(PasskeysRepositoryInterface):
    def __init__(self, connection_pool: CPool, identifier: IdentityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier
