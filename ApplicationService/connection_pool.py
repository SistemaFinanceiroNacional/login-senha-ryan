import os
import psycopg2

from ApplicationService.identity import identity


class connection_pool:
    def get_connection(self, identifier: identity):
        raise NotImplementedError()

    def get_cursor(self, identifier: identity):
        raise NotImplementedError()

class connection:
    def cursor(self):
        raise NotImplementedError


class postgresql_connection_pool(connection_pool):
    def __init__(self, createConnection=None):
        self.createConnection = createConnection or psycopg2_create_connection
        self.connections: dict[int, tuple] = dict()  # tuple[0] are connections and tuple[1] are conn's cursor

    def get_connection(self, identifier: identity):
        if identifier.value() not in self.connections.keys():
            conn = self.createConnection()
            self.connections[identifier.value()] = (conn, conn.cursor())

        return self.connections[identifier.value()][0]

    def get_cursor(self, identifier: identity):
        if identifier.value() not in self.connections.keys():
            conn = self.createConnection()
            self.connections[identifier.value()] = (conn, conn.cursor())

        return self.connections[identifier.value()][1]


def psycopg2_create_connection():
    return psycopg2.connect(os.getenv("DB_STRING_CONNECTION"))
