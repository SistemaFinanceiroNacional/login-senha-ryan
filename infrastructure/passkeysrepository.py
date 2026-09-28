from typing import List

from domain.commontypes.types import ClientID
from domain.passkey import Passkey
from infrastructure.connection_pool import ConnectionPool as CPool
from infrastructure.identityinterface import IdentityInterface
from maybe import Just, Maybe, Nothing
from usecases.repositories.passkeysrepositoryinterface import (
    PasskeysRepositoryInterface
)

COLUMNS = "p.credential_id, p.user_handle, p.public_key, p.sign_count, " \
          "p.transports"


def _passkey(credential_id, user_handle, public_key, sign_count,
             transports) -> Passkey:
    return Passkey(
        credential_id=bytes(credential_id),
        user_handle=bytes(user_handle),
        public_key=bytes(public_key),
        sign_count=sign_count,
        transports=tuple(transports),
    )


class PasskeysRepository(PasskeysRepositoryInterface):
    def __init__(self, connection_pool: CPool, identifier: IdentityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add(self, client_id: ClientID, passkey: Passkey) -> None:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute(
            "INSERT INTO passkeys (credential_id, client_id, user_handle, "
            "public_key, sign_count, transports) "
            "VALUES (%s, %s, %s, %s, %s, %s);",
            (passkey.credential_id, client_id, passkey.user_handle,
             passkey.public_key, passkey.sign_count,
             list(passkey.transports))
        )

    def of_login(self, login: str) -> List[Passkey]:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute(
            f"SELECT {COLUMNS} FROM passkeys p "
            "JOIN clients c ON c.id = p.client_id WHERE c.login = %s;",
            (login,)
        )
        return [_passkey(*row) for row in cursor.fetchall()]

    def find(self,
             login: str,
             credential_id: bytes
             ) -> Maybe[tuple[ClientID, Passkey]]:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute(
            f"SELECT p.client_id, {COLUMNS} FROM passkeys p "
            "JOIN clients c ON c.id = p.client_id "
            "WHERE c.login = %s AND p.credential_id = %s;",
            (login, credential_id)
        )
        row = cursor.fetchone()
        if row is None:
            return Nothing()
        client_id, *passkey = row
        return Just((client_id, _passkey(*passkey)))

    def update(self, passkey: Passkey) -> None:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute(
            "UPDATE passkeys SET sign_count = %s WHERE credential_id = %s;",
            (passkey.sign_count, passkey.credential_id)
        )
