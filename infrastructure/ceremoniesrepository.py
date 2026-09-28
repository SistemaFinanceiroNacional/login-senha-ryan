from infrastructure.connection_pool import ConnectionPool as CPool
from infrastructure.identityinterface import IdentityInterface
from usecases.repositories.ceremoniesrepositoryinterface import (
    CeremoniesRepositoryInterface
)


class CeremoniesRepository(CeremoniesRepositoryInterface):
    def __init__(self, connection_pool: CPool, identifier: IdentityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier
