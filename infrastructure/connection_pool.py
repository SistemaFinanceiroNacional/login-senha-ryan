from os import getenv
from psycopg2._psycopg import connection
from psycopg2 import connect
from threading import Condition
from typing import Callable
from infrastructure.identityinterface import IdentityInterface
from infrastructure.connectionInterface import (
    Cursor,
    Connection,
    ConnectionPool
)

ConnMaker = Callable[[], Connection]


def psycopg2_create_connection() -> Connection:
    class ConnectionAdapter:
        def __init__(self, conn: connection):
            self.conn = conn

        def cursor(self):
            return self.conn.cursor()

        def commit(self):
            self.conn.commit()

        def rollback(self):
            self.conn.rollback()

    return ConnectionAdapter(connect(getenv("DB_STRING_CONNECTION")))


class PostgresqlConnectionPool(ConnectionPool):
    def __init__(
            self,
            create_connection: ConnMaker = psycopg2_create_connection,
            max_connections: int = 1
    ):
        self.create_conn = create_connection
        self.used_conns: dict[int, tuple[Connection, Cursor]] = dict()
        self.max_conns = max_connections
        self.free_conns: list[tuple[Connection, Cursor]] = []
        self.condition = Condition()

    def get_connection(self, identifier: IdentityInterface) -> Connection:
        id_conn = identifier.value()
        with self.condition:
            if id_conn not in self.used_conns.keys():
                while True:
                    if self.free_conns:
                        conn_tuple = self.free_conns.pop()
                        self.used_conns[id_conn] = conn_tuple
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
