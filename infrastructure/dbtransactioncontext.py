from infrastructure.threadIdentity import IdentityInterface
from infrastructure.connection_pool import ConnectionPool as CPool
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)
from usecases.contexterrors.businesserror import BusinessError


class DBTransactionContext(TransactionContextInterface):
    def __init__(self, connection_pool: CPool, identifier: IdentityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier
        self.errors: list[BusinessError] = []

    def __enter__(self):
        self.connection_pool.get_connection(self.identifier)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        connection = self.connection_pool.get_connection(self.identifier)
        if not exc_val:
            connection.commit()

        else:
            connection.rollback()
            self.errors.append(exc_val)

        self.connection_pool.refund(self.identifier)

    def get_errors(self) -> list[BusinessError]:
        return self.errors
