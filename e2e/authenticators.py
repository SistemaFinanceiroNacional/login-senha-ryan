from playwright.sync_api import Page

PLATFORM = "internal"
SECURITY_KEY = "usb"


class VirtualAuthenticator:
    """One of Chromium's virtual FIDO2 authenticators attached to a page:
    a platform authenticator (the device's own passkeys) or an external
    security key such as a YubiKey. It answers WebAuthn requests like the
    real thing, verifying the user automatically."""

    def __init__(self, page: Page, transport: str):
        self._cdp = page.context.new_cdp_session(page)
        self._cdp.send("WebAuthn.enable")
        self.id = self._cdp.send("WebAuthn.addVirtualAuthenticator", {
            "options": {
                "protocol": "ctap2",
                "transport": transport,
                "hasResidentKey": True,
                "hasUserVerification": True,
                "isUserVerified": True,
                "automaticPresenceSimulation": True,
            }
        })["authenticatorId"]

    def credentials(self) -> list[dict]:
        return self._cdp.send(
            "WebAuthn.getCredentials", {"authenticatorId": self.id}
        )["credentials"]

    def add_credential(self, credential: dict) -> None:
        self._cdp.send("WebAuthn.addCredential", {
            "authenticatorId": self.id, "credential": credential
        })
