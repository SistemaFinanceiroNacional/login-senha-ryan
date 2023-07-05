from typing import Tuple
from password import Password as passW
from maybe import Maybe, Just, Nothing
from infrastructure.authserviceinterface import (
    AuthServiceInterface,
    ClientID
)
from infrastructure.identityinterface import (
    IdentityInterface
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as Cntx
)
from infrastructure.connection_pool import (
    ConnectionPool as CPool,
    Cursor
)


class AuthServiceDB(AuthServiceInterface):
    def __init__(self,
                 context: Cntx,
                 conn_pool: CPool,
                 identifier: IdentityInterface
                 ):
        self.transactional_context = context
        self.conn_pool = conn_pool
        self.identifier = identifier

    def authenticate(self, username: str, password: str) -> Maybe[ClientID]:
        if not username or not password:
            return Nothing()

        hash_pw = passW(password)
        with self.transactional_context:
            cursor = self.conn_pool.get_cursor(self.identifier)
            client_id = self._get_client_id(username, hash_pw, cursor)
            if client_id is not None:
                return Just(client_id[0])
            return Nothing()

    def _get_client_id(self,
                       username: str,
                       password: passW,
                       cursor: Cursor
                       ) -> Tuple | None:
        columns = "id"
        table = "clients"
        conditions = "login=%s AND password=%s"
        query = f"SELECT {columns} FROM {table} WHERE {conditions};"

        cursor.execute(query, (username, str(password)))
        find_id = cursor.fetchone()
        return find_id
