import json
from typing import Any, Dict, List

from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response
)
from webauthn.helpers import base64url_to_bytes
from webauthn.helpers.exceptions import WebAuthnException
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    AuthenticatorTransport,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement
)

from domain.passkey import Passkey
from maybe import Just, Maybe, Nothing
from usecases.passkeys.relyingpartyinterface import (
    Credential,
    RelyingPartyInterface
)

TIMEOUT_MILLISECONDS = 60000
KNOWN_TRANSPORTS = {transport.value for transport in AuthenticatorTransport}

# What an untrusted credential can make verification raise.
INVALID_CREDENTIAL = (WebAuthnException, ValueError, TypeError, KeyError)


class WebAuthnRelyingParty(RelyingPartyInterface):
    """The relying party implemented with py_webauthn.

    rp_id is the domain the passkeys are bound to and origin the exact
    origin pages are served from (scheme, host and port).

    Both platform authenticators (passkeys) and external security keys are
    accepted: no authenticator attachment is required. User verification
    (PIN, biometrics) is required; attestation is not requested."""

    def __init__(self, rp_id: str, rp_name: str, origin: str):
        self.rp_id = rp_id
        self.rp_name = rp_name
        self.origin = origin

    def registration_options(self,
                             login: str,
                             user_handle: bytes,
                             challenge: bytes
                             ) -> Dict[str, Any]:
        options = generate_registration_options(
            rp_id=self.rp_id,
            rp_name=self.rp_name,
            user_name=login,
            user_id=user_handle,
            user_display_name=login,
            challenge=challenge,
            timeout=TIMEOUT_MILLISECONDS,
            authenticator_selection=AuthenticatorSelectionCriteria(
                resident_key=ResidentKeyRequirement.PREFERRED,
                user_verification=UserVerificationRequirement.REQUIRED,
            ),
        )
        return json.loads(options_to_json(options))

    def verify_registration(self,
                            credential: Credential,
                            challenge: bytes,
                            user_handle: bytes
                            ) -> Maybe[Passkey]:
        try:
            verified = verify_registration_response(
                credential=credential,
                expected_challenge=challenge,
                expected_rp_id=self.rp_id,
                expected_origin=self.origin,
                require_user_verification=True,
            )
            transports = credential["response"].get("transports") or []
        except INVALID_CREDENTIAL:
            return Nothing()
        return Just(Passkey(
            credential_id=verified.credential_id,
            user_handle=user_handle,
            public_key=verified.credential_public_key,
            sign_count=verified.sign_count,
            transports=tuple(t for t in transports if t in KNOWN_TRANSPORTS),
        ))

    def authentication_options(self,
                               challenge: bytes,
                               passkeys: List[Passkey]
                               ) -> Dict[str, Any]:
        options = generate_authentication_options(
            rp_id=self.rp_id,
            challenge=challenge,
            timeout=TIMEOUT_MILLISECONDS,
            allow_credentials=[
                PublicKeyCredentialDescriptor(
                    id=passkey.credential_id,
                    transports=[AuthenticatorTransport(transport)
                                for transport in passkey.transports],
                )
                for passkey in passkeys
            ],
            user_verification=UserVerificationRequirement.REQUIRED,
        )
        return json.loads(options_to_json(options))

    def credential_id(self, credential: Credential) -> Maybe[bytes]:
        try:
            return Just(base64url_to_bytes(credential["rawId"]))
        except INVALID_CREDENTIAL:
            return Nothing()

    def verify_authentication(self,
                              credential: Credential,
                              challenge: bytes,
                              passkey: Passkey
                              ) -> Maybe[Passkey]:
        try:
            if not self._same_user(credential, passkey):
                return Nothing()
            verified = verify_authentication_response(
                credential=credential,
                expected_challenge=challenge,
                expected_rp_id=self.rp_id,
                expected_origin=self.origin,
                credential_public_key=passkey.public_key,
                credential_current_sign_count=passkey.sign_count,
                require_user_verification=True,
            )
        except INVALID_CREDENTIAL:
            return Nothing()
        return Just(passkey.used(verified.new_sign_count))

    @staticmethod
    def _same_user(credential: Credential, passkey: Passkey) -> bool:
        user_handle = credential["response"].get("userHandle")
        return not user_handle or \
            base64url_to_bytes(user_handle) == passkey.user_handle
