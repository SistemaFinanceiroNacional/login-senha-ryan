from Infrastructure.threadIdentity import identityInterface
from Infrastructure.connection_pool import connection_pool as cpool
from ApplicationService.repositories.transactioncontextinterface import (
    TransactionContextInterface
)
from ApplicationService.contexterrors.businesserror import BusinessError


class dbTransactionContext(TransactionContextInterface):
    def __init__(self, connection_pool: cpool, identifier: identityInterface):
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
