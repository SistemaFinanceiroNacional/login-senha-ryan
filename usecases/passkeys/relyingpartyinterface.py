from typing import Any, Dict, List

from domain.passkey import Passkey
from maybe import Maybe

Credential = Dict[str, Any]


class RelyingPartyInterface:
    """The WebAuthn relying party: builds the options sent to the browser
    and verifies what authenticators answer."""

    def registration_options(self,
                             login: str,
                             user_handle: bytes,
                             challenge: bytes
                             ) -> Dict[str, Any]:
        raise NotImplementedError

    def verify_registration(self,
                            credential: Credential,
                            challenge: bytes,
                            user_handle: bytes
                            ) -> Maybe[Passkey]:
        raise NotImplementedError

    def authentication_options(self,
                               challenge: bytes,
                               passkeys: List[Passkey]
                               ) -> Dict[str, Any]:
        raise NotImplementedError

    def credential_id(self, credential: Credential) -> Maybe[bytes]:
        raise NotImplementedError

    def verify_authentication(self,
                              credential: Credential,
                              challenge: bytes,
                              passkey: Passkey
                              ) -> Maybe[Passkey]:
        """The passkey with its updated signature counter, when the
        assertion is valid."""
        raise NotImplementedError
