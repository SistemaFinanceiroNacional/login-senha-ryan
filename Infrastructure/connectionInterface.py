from typing import Protocol, Tuple, List
from Infrastructure.identityinterface import IdentityInterface


class Cursor(Protocol):
    def execute(self, *args) -> None:
        raise NotImplementedError

    def fetchone(self) -> None | Tuple:
        raise NotImplementedError

    def fetchall(self) -> List:
        raise NotImplementedError


class Connection(Protocol):
    def cursor(self) -> Cursor:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


class ConnectionPool:
    def get_connection(self, identifier: IdentityInterface) -> Connection:
        raise NotImplementedError()

    def get_cursor(self, identifier: IdentityInterface) -> Cursor:
        raise NotImplementedError()

    def refund(self, identifier: IdentityInterface) -> None:
        raise NotImplementedError()
