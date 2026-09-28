import hashlib
from datetime import timedelta

from psycopg2.extras import Json

from drivers.web.framework.httprequest.sessionstore import (
    SessionData,
    SessionStoreInterface
)
from infrastructure.connection_pool import ConnectionPool as CPool
from infrastructure.identityinterface import IdentityInterface
from maybe import Just, Maybe, Nothing
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)


def _hash(token: str) -> bytes:
    return hashlib.sha256(token.encode()).digest()


class DBSessionStore(SessionStoreInterface):
    """Sessions in PostgreSQL. A session ends after `idle_timeout` without
    requests or `lifetime` after it started, whichever comes first. Only
    the SHA-256 of each token is stored."""

    def __init__(self,
                 context: TransactionContextInterface,
                 connection_pool: CPool,
                 identifier: IdentityInterface,
                 idle_timeout: timedelta,
                 lifetime: timedelta
                 ):
        self.context = context
        self.connection_pool = connection_pool
        self.identifier = identifier
        self.idle_timeout = idle_timeout
        self.lifetime = lifetime

    def load(self, token: str) -> Maybe[SessionData]:
        with self.context:
            cursor = self.connection_pool.get_cursor(self.identifier)
            cursor.execute(
                "SELECT data FROM sessions "
                "WHERE token_hash = %s AND expires_at > now() "
                "AND created_at + %s > now();",
                (_hash(token), self.lifetime)
            )
            row = cursor.fetchone()
        if row is None:
            return Nothing()
        return Just(row[0])

    def save(self, token: str, data: SessionData) -> None:
        with self.context:
            cursor = self.connection_pool.get_cursor(self.identifier)
            cursor.execute("DELETE FROM sessions WHERE expires_at <= now();")
            cursor.execute(
                "INSERT INTO sessions (token_hash, data, expires_at) "
                "VALUES (%s, %s, now() + %s) "
                "ON CONFLICT (token_hash) DO UPDATE "
                "SET data = EXCLUDED.data, expires_at = EXCLUDED.expires_at;",
                (_hash(token), Json(data), self.idle_timeout)
            )

    def delete(self, token: str) -> None:
        with self.context:
            cursor = self.connection_pool.get_cursor(self.identifier)
            cursor.execute(
                "DELETE FROM sessions WHERE token_hash = %s;", (_hash(token),)
            )
