import base64
import hashlib
import json
import os
import struct
from typing import Dict, Optional

import cbor2
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

USER_PRESENT = 0x01
USER_VERIFIED = 0x04
ATTESTED_CREDENTIAL_DATA = 0x40


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def from_b64url(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


class NoCredential(Exception):
    """What a browser reports as NotAllowedError: this authenticator has no
    credential the relying party accepts."""


class _Credential:
    def __init__(self, rp_id: str, user_handle: bytes):
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.rp_id = rp_id
        self.user_handle = user_handle
        self.sign_count = 0


class SoftwareAuthenticator:
    """A FIDO2 authenticator in software, together with the browser side of
    WebAuthn: real ES256 key pairs, real signatures and the CTAP2 data
    formats ("none" attestation). It lets use case tests run complete
    ceremonies against the real relying party code; end-to-end tests use
    Chromium's virtual authenticators instead.

    `origin` is the page the browser is on; changing it models a phishing
    site relaying the ceremony."""

    def __init__(self, origin: str, attachment: str = "cross-platform"):
        self.origin = origin
        self.attachment = attachment
        self._credentials: Dict[bytes, _Credential] = {}

    def create(self, options: dict) -> dict:
        """navigator.credentials.create() with the options the server
        sent, returning the credential as the page posts it back."""
        rp_id = options["rp"]["id"]
        credential_id = os.urandom(32)
        credential = _Credential(rp_id, from_b64url(options["user"]["id"]))
        self._credentials[credential_id] = credential

        public = credential.private_key.public_key().public_numbers()
        cose_key = {1: 2, 3: -7, -1: 1,
                    -2: public.x.to_bytes(32, "big"),
                    -3: public.y.to_bytes(32, "big")}
        attested_credential = bytes(16) \
            + struct.pack(">H", len(credential_id)) + credential_id \
            + cbor2.dumps(cose_key)
        flags = USER_PRESENT | USER_VERIFIED | ATTESTED_CREDENTIAL_DATA
        authenticator_data = self._authenticator_data(rp_id, flags, 0) \
            + attested_credential
        attestation = cbor2.dumps(
            {"fmt": "none", "attStmt": {}, "authData": authenticator_data}
        )
        client_data = self._client_data("webauthn.create",
                                        options["challenge"])
        return {
            "id": b64url(credential_id),
            "rawId": b64url(credential_id),
            "type": "public-key",
            "authenticatorAttachment": self.attachment,
            "clientExtensionResults": {},
            "response": {
                "clientDataJSON": b64url(client_data),
                "attestationObject": b64url(attestation),
                "transports": self._transports(),
            },
        }

    def get(self, options: dict,
            credential_id: Optional[bytes] = None) -> dict:
        """navigator.credentials.get(). A malicious client may pick the
        credential itself, ignoring the server's allow list."""
        rp_id = options["rpId"]
        allowed = [from_b64url(c["id"])
                   for c in options.get("allowCredentials", [])]
        if credential_id is None:
            credential_id = self._pick(rp_id, allowed)
        credential = self._credentials[credential_id]
        credential.sign_count += 1

        authenticator_data = self._authenticator_data(
            rp_id, USER_PRESENT | USER_VERIFIED, credential.sign_count
        )
        client_data = self._client_data("webauthn.get", options["challenge"])
        signature = credential.private_key.sign(
            authenticator_data + hashlib.sha256(client_data).digest(),
            ec.ECDSA(hashes.SHA256())
        )
        return {
            "id": b64url(credential_id),
            "rawId": b64url(credential_id),
            "type": "public-key",
            "authenticatorAttachment": self.attachment,
            "clientExtensionResults": {},
            "response": {
                "clientDataJSON": b64url(client_data),
                "authenticatorData": b64url(authenticator_data),
                "signature": b64url(signature),
                "userHandle": b64url(credential.user_handle),
            },
        }

    def credential_ids(self) -> list[bytes]:
        return list(self._credentials)

    def rewind_sign_count(self, credential_id: bytes) -> None:
        """What a cloned authenticator looks like to the server."""
        self._credentials[credential_id].sign_count = 0

    def _pick(self, rp_id: str, allowed: list[bytes]) -> bytes:
        for credential_id, credential in self._credentials.items():
            if credential.rp_id == rp_id and \
                    (not allowed or credential_id in allowed):
                return credential_id
        raise NoCredential()

    def _transports(self) -> list[str]:
        return ["internal"] if self.attachment == "platform" else ["usb"]

    def _client_data(self, kind: str, challenge: str) -> bytes:
        return json.dumps({
            "type": kind,
            "challenge": challenge,
            "origin": self.origin,
            "crossOrigin": False,
        }).encode()

    @staticmethod
    def _authenticator_data(rp_id: str, flags: int, sign_count: int) -> bytes:
        return hashlib.sha256(rp_id.encode()).digest() \
            + bytes([flags]) + struct.pack(">I", sign_count)
