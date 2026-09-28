from domain.commontypes.types import ClientID
from domain.passkey import Passkey
from maybe import Just, Maybe, Nothing
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


class StartPasskeyAuthentication:
    """A client asks to sign in under a login."""

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

    def execute(self, login: str) -> Maybe[CeremonyOptions]:
        return valid_login(login).flat_map(self._start)

    def _start(self, login: str) -> Maybe[CeremonyOptions]:
        with self._context:
            passkeys = self._passkeys.of_login(login)
            if not passkeys:
                return Nothing()
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
