from infrastructure.threadIdentity import IdentityInterface
from infrastructure.connection_pool import ConnectionPool as CPool
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)
from usecases.contexterrors.businesserror import BusinessError


class DBTransactionContext(TransactionContextInterface):
    """One database transaction per `with` block. get_errors() reports the
    errors of the last block run by the calling thread only: the context
    is shared by every use case and every thread."""

    def __init__(self, connection_pool: CPool, identifier: IdentityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier
        self._errors: dict[int, list[BusinessError]] = {}

    def __enter__(self):
        self._errors[self.identifier.value()] = []
        self.connection_pool.get_connection(self.identifier)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        connection = self.connection_pool.get_connection(self.identifier)
        if not exc_val:
            connection.commit()

        else:
            connection.rollback()
            self._errors[self.identifier.value()].append(exc_val)

        self.connection_pool.refund(self.identifier)

    def get_errors(self) -> list[BusinessError]:
        return self._errors.get(self.identifier.value(), [])
