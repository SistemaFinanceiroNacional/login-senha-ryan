from ApplicationService.repositories.clientsrepositoryinterface import(
    ClientsRepositoryInterface,
    pw
)
from ApplicationService.repositories.identityinterface import (
    identityInterface
)
from Infrastructure.connection_pool import (
    connection_pool as cpool
)


class ClientsRepository(ClientsRepositoryInterface):
    def __init__(self, connection_pool: cpool, identifier: identityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add_client(self, new_login: str, new_password: pw) -> bool:
        cursor = self.connection_pool.get_cursor(self.identifier)
        query = "SELECT * FROM clients WHERE login = %s;"
        cursor.execute(query, (new_login,))
        account_query_result = cursor.fetchone()

        if not account_query_result:
            columns = "(login,password)"
            statements = "VALUES (%s,%s)"
            return_t = "RETURNING id"
            query = f"INSERT INTO clients {columns} {statements} {return_t};"
            cursor.execute(query, (new_login, str(new_password)))

            client_id = cursor.fetchone()

            statements = "VALUES (default)"
            query = f"INSERT INTO accounts {statements} {return_t};"
            cursor.execute(query)
            account_id = cursor.fetchone()[0]

            columns = "(client_id, account_id)"
            statements = "VALUES (%s,%s)"
            table = "clients_accounts"
            query = f"INSERT INTO {table} {columns} {statements};"
            cursor.execute(query, (client_id, account_id))

        return not account_query_result
