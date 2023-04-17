from typing import Protocol
from ApplicationService.repositories.identity import identity

class cursor(Protocol):
    def execute(self, *args) -> None:
        raise NotImplementedError

    def fetchone(self) -> None or tuple:
        raise NotImplementedError

class connection(Protocol):
    def cursor(self) -> cursor:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError

class connection_pool:
    def get_connection(self, identifier: identity) -> connection:
        raise NotImplementedError()

    def get_cursor(self, identifier: identity) -> cursor:
        raise NotImplementedError()

    def refund(self, identifier: identity) -> None:
        raise NotImplementedError()