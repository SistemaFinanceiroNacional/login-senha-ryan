from domain.commontypes.types import ClientID
from maybe import Just, Maybe, Nothing
from usecases.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface
)
from infrastructure.identityinterface import (
    IdentityInterface
)
from infrastructure.connection_pool import (
    ConnectionPool as CPool
)


class ClientsRepository(ClientsRepositoryInterface):
    def __init__(self, connection_pool: CPool, identifier: IdentityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def login_taken(self, login: str) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT 1 FROM clients WHERE login = %s;", (login,))
        return cursor.fetchone() is not None

    def add_passwordless_client(self, login: str) -> Maybe[ClientID]:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute(
            "INSERT INTO clients (login) VALUES (%s) "
            "ON CONFLICT (login) DO NOTHING RETURNING id;",
            (login,)
        )
        row = cursor.fetchone()
        if row is None:
            return Nothing()
        client_id = row[0]
        self._open_account(client_id)
        return Just(client_id)

    def _open_account(self, client_id) -> None:
        cursor = self.connection_pool.get_cursor(self.identifier)
        return_t = "RETURNING id"
        statements = "VALUES (default)"
        query = f"INSERT INTO accounts {statements} {return_t};"
        cursor.execute(query)
        fetchone = cursor.fetchone()
        if fetchone is None:
            raise Exception("WTF: ID must not be null after an insertion.")
        account_id = fetchone[0]

        columns = "(client_id, account_id)"
        statements = "VALUES (%s,%s)"
        table = "clients_accounts"
        query = f"INSERT INTO {table} {columns} {statements};"
        cursor.execute(query, (client_id, account_id))
