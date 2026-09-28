import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, NamedTuple, Optional

from domain.commontypes.types import ClientID
from maybe import Just, Maybe, Nothing

CEREMONY_LIFETIME = timedelta(minutes=5)


class CeremonyKind(Enum):
    REGISTRATION = "registration"
    AUTHENTICATION = "authentication"


@dataclass(frozen=True)
class Ceremony:
    """A WebAuthn registration or authentication in progress: the challenge
    the authenticator has to sign, kept on the server."""
    id: str
    kind: CeremonyKind
    login: str
    challenge: bytes
    user_handle: Optional[bytes]
    expires_at: datetime

    @staticmethod
    def begin(kind: CeremonyKind,
              login: str,
              user_handle: Optional[bytes] = None
              ) -> "Ceremony":
        return Ceremony(
            id=str(uuid.uuid4()),
            kind=kind,
            login=login,
            challenge=secrets.token_bytes(32),
            user_handle=user_handle,
            expires_at=datetime.now(timezone.utc) + CEREMONY_LIFETIME,
        )


class CeremonyOptions(NamedTuple):
    """What the browser needs to run a ceremony: its id, to finish it, and
    the WebAuthn options for navigator.credentials."""
    ceremony_id: str
    public_key: Dict[str, Any]


class SignedInClient(NamedTuple):
    id: ClientID
    login: str


MAX_LOGIN_LENGTH = 64


def valid_login(login) -> Maybe[str]:
    if not isinstance(login, str):
        return Nothing()
    login = login.strip()
    if 0 < len(login) <= MAX_LOGIN_LENGTH:
        return Just(login)
    return Nothing()
