import uuid

from infrastructure.connection_pool import ConnectionPool as CPool
from infrastructure.identityinterface import IdentityInterface
from maybe import Just, Maybe, Nothing
from usecases.passkeys.ceremony import Ceremony, CeremonyKind
from usecases.repositories.ceremoniesrepositoryinterface import (
    CeremoniesRepositoryInterface
)


class CeremoniesRepository(CeremoniesRepositoryInterface):
    def __init__(self, connection_pool: CPool, identifier: IdentityInterface):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def start(self, ceremony: Ceremony) -> None:
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute(
            "DELETE FROM webauthn_ceremonies WHERE expires_at <= now();"
        )
        cursor.execute(
            "INSERT INTO webauthn_ceremonies "
            "(id, kind, login, challenge, user_handle, expires_at) "
            "VALUES (%s, %s, %s, %s, %s, %s);",
            (ceremony.id, ceremony.kind.value, ceremony.login,
             ceremony.challenge, ceremony.user_handle, ceremony.expires_at)
        )

    def consume(self, ceremony_id: str, kind: CeremonyKind) -> Maybe[Ceremony]:
        try:
            uuid.UUID(ceremony_id)
        except (TypeError, ValueError, AttributeError):
            return Nothing()

        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute(
            "DELETE FROM webauthn_ceremonies "
            "WHERE id = %s AND kind = %s AND expires_at > now() "
            "RETURNING login, challenge, user_handle, expires_at;",
            (ceremony_id, kind.value)
        )
        row = cursor.fetchone()
        if row is None:
            return Nothing()
        login, challenge, user_handle, expires_at = row
        return Just(Ceremony(
            id=ceremony_id,
            kind=kind,
            login=login,
            challenge=bytes(challenge),
            user_handle=bytes(user_handle) if user_handle else None,
            expires_at=expires_at,
        ))
