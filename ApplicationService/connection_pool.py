from os import getenv
from psycopg2 import connect
from threading import Condition
from typing import Callable
from ApplicationService.repositories.identity import identity
from ApplicationService.repositories.connectionInterface import cursor, connection, connection_pool


class postgresql_connection_pool(connection_pool):
    def __init__(self, createConnection: Callable[[], connection] = None, max_connections: int = 1, condition=None):
        self.create_connection = createConnection or psycopg2_create_connection
        self.allocated_connections: dict[int, tuple[connection, cursor]] = dict()
        self.max_connections = max_connections
        self.free_connections: list[tuple[connection, cursor]] = []
        self.condition = condition() if condition else Condition()

    def get_connection(self, identifier: identity) -> connection:
        id_conn = identifier.value()
        with self.condition:
            if id_conn not in self.allocated_connections.keys():
                while True:
                    if self.free_connections:
                        conn = self.free_connections.pop()
                        self.allocated_connections[id_conn] = conn
                        break

                    elif len(self.allocated_connections) < self.max_connections:
                        conn = self.create_connection()
                        self.allocated_connections[id_conn] = (conn, conn.cursor())
                        break

                    else:
                        self.condition.wait()

            return self.allocated_connections[id_conn][0]

    def get_cursor(self, identifier: identity) -> cursor:
        id_conn = identifier.value()
        with self.condition:
            if id_conn not in self.allocated_connections.keys():
                conn = self.create_connection()
                self.allocated_connections[id_conn] = (conn, conn.cursor())

        return self.allocated_connections[id_conn][1]

    def refund(self, identifier: identity) -> None:
        with self.condition:
            if identifier.value() in self.allocated_connections.keys():
                conn = self.allocated_connections.pop(identifier.value())
                self.free_connections.append(conn)
                self.condition.notify_all()


def psycopg2_create_connection() -> connection:
    return connect(getenv("DB_STRING_CONNECTION"))
