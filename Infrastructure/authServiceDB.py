from password import Password as pw
from maybe import maybe, just, nothing
from Infrastructure.authserviceinterface import (
    AuthServiceInterface,
    ClientID
)
from ApplicationService.repositories.identityinterface import (
    identityInterface
)
from ApplicationService.repositories.transactioncontextinterface import (
    TransactionContextInterface as cntx
)
from Infrastructure.connection_pool import (
    connection_pool as c_pool,
    cursor as c
)


class AuthServiceDB(AuthServiceInterface):
    def __init__(self,
                 context: cntx,
                 conn_pool: c_pool,
                 identifier: identityInterface
                 ):
        self.transactional_context = context
        self.conn_pool = conn_pool
        self.identifier = identifier

    def authenticate(self, username: str, password: str) -> maybe[ClientID]:
        if not username or not password:
            return nothing()

        hash_pw = pw(password)
        with self.transactional_context:
            cursor = self.conn_pool.get_cursor(self.identifier)
            client_id = self._get_client_id(username, hash_pw, cursor)
            if client_id is not None:
                return just(client_id[0])
            return nothing()

    def _get_client_id(self,
                       username: str,
                       password: pw,
                       cursor: c
                       ) -> int or None:
        columns = "id"
        table = "clients"
        conditions = "login=%s AND password=%s"
        query = f"SELECT {columns} FROM {table} WHERE {conditions};"

        cursor.execute(query, (username, str(password)))
        find_id = cursor.fetchone()
        return find_id
