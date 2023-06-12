from os import getenv
from psycopg2 import connect
from threading import Condition
from typing import Callable
from Infrastructure.identityinterface import IdentityInterface
from Infrastructure.connectionInterface import (
    Cursor,
    Connection,
    ConnectionPool
)


class PostgresqlConnectionPool(ConnectionPool):
    def __init__(
            self,
            create_connection: Callable[[], Connection] = None,
            max_connections: int = 1,
            condition=None
    ):
        self.create_conn = create_connection or psycopg2_create_connection
        self.used_conns: dict[int, tuple[Connection, Cursor]] = dict()
        self.max_conns = max_connections
        self.free_conns: list[tuple[Connection, Cursor]] = []
        self.condition = condition() if condition else Condition()

    def get_connection(self, identifier: IdentityInterface) -> Connection:
        id_conn = identifier.value()
        with self.condition:
            if id_conn not in self.used_conns.keys():
                while True:
                    if self.free_conns:
                        conn = self.free_conns.pop()
                        self.used_conns[id_conn] = conn
                        break

                    elif len(self.used_conns) < self.max_conns:
                        conn = self.create_conn()
                        self.used_conns[id_conn] = (conn, conn.cursor())
                        break

                    else:
                        self.condition.wait()

            return self.used_conns[id_conn][0]

    def get_cursor(self, identifier: IdentityInterface) -> Cursor:
        id_conn = identifier.value()
        with self.condition:
            if id_conn not in self.used_conns.keys():
                conn = self.create_conn()
                self.used_conns[id_conn] = (conn, conn.cursor())

        return self.used_conns[id_conn][1]

    def refund(self, identifier: IdentityInterface) -> None:
        with self.condition:
            if identifier.value() in self.used_conns.keys():
                conn = self.used_conns.pop(identifier.value())
                self.free_conns.append(conn)
                self.condition.notify_all()


def psycopg2_create_connection() -> Connection:
    return connect(getenv("DB_STRING_CONNECTION"))
