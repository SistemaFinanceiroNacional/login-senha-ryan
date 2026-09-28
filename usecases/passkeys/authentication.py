import hmac

from domain.commontypes.types import ClientID
from domain.passkey import Passkey
from maybe import Just, Maybe
from usecases.passkeys.ceremony import (
    Ceremony,
    CeremonyKind,
    CeremonyOptions,
    SignedInClient,
    valid_login
)
from usecases.passkeys.relyingpartyinterface import (
    Credential,
    RelyingPartyInterface
)
from usecases.repositories.ceremoniesrepositoryinterface import (
    CeremoniesRepositoryInterface
)
from usecases.repositories.passkeysrepositoryinterface import (
    PasskeysRepositoryInterface
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)


def decoy_passkey(decoy_key: bytes, login: str) -> Passkey:
    """A credential that looks registered for a login that is not: always
    the same for the same login, so asking again gives nothing away."""
    credential_id = hmac.new(decoy_key, login.encode(), "sha256").digest()
    return Passkey(credential_id=credential_id, user_handle=b"",
                   public_key=b"", sign_count=0, transports=("internal",))


class StartPasskeyAuthentication:
    """A client asks to sign in under a login.

    Whether the login exists is not revealed: an unknown login gets a
    ceremony too, allowing a decoy credential that can never sign in."""

    def __init__(self,
                 passkeys: PasskeysRepositoryInterface,
                 ceremonies: CeremoniesRepositoryInterface,
                 relying_party: RelyingPartyInterface,
                 context: TransactionContextInterface,
                 decoy_key: bytes
                 ):
        self._passkeys = passkeys
        self._ceremonies = ceremonies
        self._relying_party = relying_party
        self._context = context
        self._decoy_key = decoy_key

    def execute(self, login: str) -> Maybe[CeremonyOptions]:
        return valid_login(login).flat_map(self._start)

    def _start(self, login: str) -> Maybe[CeremonyOptions]:
        with self._context:
            passkeys = self._passkeys.of_login(login) or \
                [decoy_passkey(self._decoy_key, login)]
            ceremony = Ceremony.begin(CeremonyKind.AUTHENTICATION, login)
            self._ceremonies.start(ceremony)

        options = self._relying_party.authentication_options(
            ceremony.challenge, passkeys
        )
        return Just(CeremonyOptions(ceremony.id, options))


class FinishPasskeyAuthentication:
    """The client's authenticator signed the challenge."""

    def __init__(self,
                 passkeys: PasskeysRepositoryInterface,
                 ceremonies: CeremoniesRepositoryInterface,
                 relying_party: RelyingPartyInterface,
                 context: TransactionContextInterface
                 ):
        self._passkeys = passkeys
        self._ceremonies = ceremonies
        self._relying_party = relying_party
        self._context = context

    def execute(self,
                ceremony_id: str,
                credential: Credential
                ) -> Maybe[SignedInClient]:
        with self._context:
            return self._ceremonies.consume(
                ceremony_id, CeremonyKind.AUTHENTICATION
            ).flat_map(lambda ceremony: self._sign_in(ceremony, credential))

    def _sign_in(self,
                 ceremony: Ceremony,
                 credential: Credential
                 ) -> Maybe[SignedInClient]:
        return self._relying_party.credential_id(credential).flat_map(
            lambda credential_id: self._passkeys.find(
                ceremony.login, credential_id
            )
        ).flat_map(
            lambda found: self._verify(ceremony, credential, *found)
        )

    def _verify(self,
                ceremony: Ceremony,
                credential: Credential,
                client_id: ClientID,
                passkey: Passkey
                ) -> Maybe[SignedInClient]:
        return self._relying_party.verify_authentication(
            credential, ceremony.challenge, passkey
        ).run(self._passkeys.update).map(
            lambda _: SignedInClient(client_id, ceremony.login)
        )
