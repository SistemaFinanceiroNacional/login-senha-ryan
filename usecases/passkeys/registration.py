import secrets

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
from usecases.repositories.clientsrepositoryinterface import (
    ClientsRepositoryInterface
)
from usecases.repositories.passkeysrepositoryinterface import (
    PasskeysRepositoryInterface
)
from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface
)


class StartPasskeyRegistration:
    """A new client asks to register with a passkey under a login."""

    def __init__(self,
                 clients: ClientsRepositoryInterface,
                 ceremonies: CeremoniesRepositoryInterface,
                 relying_party: RelyingPartyInterface,
                 context: TransactionContextInterface
                 ):
        self._clients = clients
        self._ceremonies = ceremonies
        self._relying_party = relying_party
        self._context = context

    def execute(self, login: str) -> Maybe[CeremonyOptions]:
        return valid_login(login).flat_map(self._start)

    def _start(self, login: str) -> Maybe[CeremonyOptions]:
        with self._context:
            if self._clients.login_taken(login):
                return Nothing()
            ceremony = Ceremony.begin(
                CeremonyKind.REGISTRATION, login, secrets.token_bytes(32)
            )
            self._ceremonies.start(ceremony)

        options = self._relying_party.registration_options(
            login, ceremony.user_handle or b"", ceremony.challenge
        )
        return Just(CeremonyOptions(ceremony.id, options))


class FinishPasskeyRegistration:
    """The new client's authenticator created a credential: the client and
    their first account exist from now on, and they are signed in."""

    def __init__(self,
                 clients: ClientsRepositoryInterface,
                 passkeys: PasskeysRepositoryInterface,
                 ceremonies: CeremoniesRepositoryInterface,
                 relying_party: RelyingPartyInterface,
                 context: TransactionContextInterface
                 ):
        self._clients = clients
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
                ceremony_id, CeremonyKind.REGISTRATION
            ).flat_map(lambda ceremony: self._register(ceremony, credential))

    def _register(self,
                  ceremony: Ceremony,
                  credential: Credential
                  ) -> Maybe[SignedInClient]:
        return self._relying_party.verify_registration(
            credential, ceremony.challenge, ceremony.user_handle or b""
        ).flat_map(lambda passkey: self._new_client(ceremony.login, passkey))

    def _new_client(self,
                    login: str,
                    passkey: Passkey
                    ) -> Maybe[SignedInClient]:
        return self._clients.add_passwordless_client(login).run(
            lambda client_id: self._passkeys.add(client_id, passkey)
        ).map(lambda client_id: SignedInClient(client_id, login))
