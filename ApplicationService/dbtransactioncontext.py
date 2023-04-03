from typing import Any
from ApplicationService.threadIdentity import identity
from ApplicationService.connection_pool import connection_pool as cpool
from ApplicationService.transactioncontext import transactioncontext

class dbTransactionContext(transactioncontext):
    def __init__(self, connection_pool: cpool, identifier: identity):
        self.connection_pool = connection_pool
        self.identifier = identifier
        self.errors: list[Any] = []

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

    def get_errors(self):
        return self.errors