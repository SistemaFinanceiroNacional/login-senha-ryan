from dataclasses import dataclass, replace
from typing import Tuple


@dataclass(frozen=True)
class Passkey:
    """A FIDO2/WebAuthn credential registered by a client: a platform
    passkey or an external security key. The server only ever holds its
    public key."""
    credential_id: bytes
    user_handle: bytes
    public_key: bytes
    sign_count: int
    transports: Tuple[str, ...] = ()

    def used(self, sign_count: int) -> "Passkey":
        return replace(self, sign_count=sign_count)
