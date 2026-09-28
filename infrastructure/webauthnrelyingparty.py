from usecases.passkeys.relyingpartyinterface import RelyingPartyInterface


class WebAuthnRelyingParty(RelyingPartyInterface):
    """The relying party implemented with py_webauthn.

    rp_id is the domain the passkeys are bound to and origin the exact
    origin pages are served from (scheme, host and port)."""

    def __init__(self, rp_id: str, rp_name: str, origin: str):
        self.rp_id = rp_id
        self.rp_name = rp_name
        self.origin = origin
