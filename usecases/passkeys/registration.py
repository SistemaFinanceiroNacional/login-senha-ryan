from maybe import Maybe
from usecases.passkeys.ceremony import CeremonyOptions, SignedInClient
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
        raise NotImplementedError


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
        raise NotImplementedError
