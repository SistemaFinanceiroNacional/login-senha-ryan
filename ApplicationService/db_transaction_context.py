from typing import Any


class db_transaction_context:
    def __init__(self, connection_pool, identity):
        self.connection_pool = connection_pool
        self.identity = identity
        self.errors: list[Any] = []

    def __enter__(self):
        connection = self.connection_pool.get_connection(self.identity)
        connection.start_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        connection = self.connection_pool.get_connection(self.identity)
        if not exc_val:
            connection.commit()

        else:
            connection.rollback()
            self.errors.append(exc_val)

        self.connection_pool.refund(self.identity)

    def get_errors(self):
        return self.errors