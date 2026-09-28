from maybe import Maybe
from usecases.passkeys.ceremony import CeremonyOptions, SignedInClient
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
        raise NotImplementedError


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
        raise NotImplementedError
