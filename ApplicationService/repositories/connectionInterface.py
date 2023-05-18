from typing import Protocol, Tuple, List
from ApplicationService.repositories.identityinterface import identityInterface


class cursor(Protocol):
    def execute(self, *args) -> None:
        raise NotImplementedError

    def fetchone(self) -> None or Tuple:
        raise NotImplementedError

    def fetchall(self) -> List:
        raise NotImplementedError


class connection(Protocol):
    def cursor(self) -> cursor:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


class connection_pool:
    def get_connection(self, identifier: identityInterface) -> connection:
        raise NotImplementedError()

    def get_cursor(self, identifier: identityInterface) -> cursor:
        raise NotImplementedError()

    def refund(self, identifier: identityInterface) -> None:
        raise NotImplementedError()
