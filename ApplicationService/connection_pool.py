import os
import psycopg2
import threading
from ApplicationService.identity import identity


class connection_pool:
    def get_connection(self, identifier: identity):
        raise NotImplementedError()

    def get_cursor(self, identifier: identity):
        raise NotImplementedError()

    def refund(self, identifier: identity):
        raise NotImplementedError()

class connection:
    def cursor(self):
        raise NotImplementedError


class postgresql_connection_pool(connection_pool):
    def __init__(self, createConnection=None, max_connections=1, condition=None):
        self.create_connection = createConnection or psycopg2_create_connection
        self.connections: dict[int, tuple] = dict()  # tuple[0] are connections and tuple[1] are conn's cursor
        self.max_connections = max_connections
        self.free_connections = []
        self.condition = condition() if condition else threading.Condition()

    def get_connection(self, identifier: identity):
        id_conn = identifier.value()
        with self.condition:
            if id_conn not in self.connections.keys():
                while True:
                    if self.free_connections:
                        conn = self.free_connections.pop()
                        self.connections[id_conn] = (conn, conn.cursor())
                        break

                    elif len(self.connections) < self.max_connections:
                        conn = self.create_connection()
                        self.connections[id_conn] = (conn, conn.cursor())
                        break

                    else:
                        self.condition.wait()

            return self.connections[id_conn][0]

    def get_cursor(self, identifier: identity):
        if identifier.value() not in self.connections.keys():
            conn = self.create_connection()
            self.connections[identifier.value()] = (conn, conn.cursor())

        return self.connections[identifier.value()][1]

    def refund(self, identifier: identity):
        with self.condition:
            if identifier.value() in self.connections.keys():
                conn = self.connections.pop(identifier.value())[0]
                self.free_connections.append(conn)
                self.condition.notify_all()


def psycopg2_create_connection():
    return psycopg2.connect(os.getenv("DB_STRING_CONNECTION"))
