from os import getenv
from psycopg2 import connect
from threading import Condition
from typing import Callable
from ApplicationService.repositories.identityinterface import identityInterface
from ApplicationService.repositories.connectionInterface import (
    cursor,
    connection,
    connection_pool
)


class postgresql_connection_pool(connection_pool):
    def __init__(
            self,
            createConnection: Callable[[], connection] = None,
            max_connections: int = 1,
            condition=None
    ):
        self.create_connection = createConnection or psycopg2_create_connection
        self.used_connections: dict[int, tuple[connection, cursor]] = dict()
        self.max_connections = max_connections
        self.free_connections: list[tuple[connection, cursor]] = []
        self.condition = condition() if condition else Condition()

    def get_connection(self, identifier: identityInterface) -> connection:
        id_conn = identifier.value()
        with self.condition:
            if id_conn not in self.used_connections.keys():
                while True:
                    if self.free_connections:
                        conn = self.free_connections.pop()
                        self.used_connections[id_conn] = conn
                        break

                    elif len(self.used_connections) < self.max_connections:
                        conn = self.create_connection()
                        self.used_connections[id_conn] = (conn, conn.cursor())
                        break

                    else:
                        self.condition.wait()

            return self.used_connections[id_conn][0]

    def get_cursor(self, identifier: identityInterface) -> cursor:
        id_conn = identifier.value()
        with self.condition:
            if id_conn not in self.used_connections.keys():
                conn = self.create_connection()
                self.used_connections[id_conn] = (conn, conn.cursor())

        return self.used_connections[id_conn][1]

    def refund(self, identifier: identityInterface) -> None:
        with self.condition:
            if identifier.value() in self.used_connections.keys():
                conn = self.used_connections.pop(identifier.value())
                self.free_connections.append(conn)
                self.condition.notify_all()


def psycopg2_create_connection() -> connection:
    return connect(getenv("DB_STRING_CONNECTION"))
