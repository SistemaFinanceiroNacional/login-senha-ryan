from typing import NamedTuple

from domain.commontypes.types import AccountID, ClientID
from infrastructure.accountsrepository import AccountsRepository
from infrastructure.authservicedb import AuthServiceDB
from infrastructure.ceremoniesrepository import CeremoniesRepository
from infrastructure.clientsrepository import ClientsRepository
from infrastructure.connection_pool import (
    PostgresqlConnectionPool,
    psycopg2_create_connection
)
from infrastructure.dbtransactioncontext import DBTransactionContext
from infrastructure.passkeysrepository import PasskeysRepository
from infrastructure.threadIdentity import ThreadIdentity
from infrastructure.webauthnrelyingparty import WebAuthnRelyingParty
from maybe import Maybe
from testsupport.authenticator import SoftwareAuthenticator
from password import Password
from usecases.deposit import DepositUseCase
from usecases.new_bank_account import NewBankAccountUseCase
from usecases.transfer import TransferFundsUseCase
from usecases.get_accounts import GetAccountsUseCase
from usecases.get_balance import GetBalanceUseCase
from usecases.get_transactions import GetTransactionsUseCase
from usecases.passkeys.authentication import (
    FinishPasskeyAuthentication,
    StartPasskeyAuthentication
)
from usecases.passkeys.ceremony import SignedInClient
from usecases.passkeys.registration import (
    FinishPasskeyRegistration,
    StartPasskeyRegistration
)
from usecases.register_client import RegisterClientUseCase

PASSWORD = "secret"
RP_ID = "localhost"
ORIGIN = "http://localhost:8080"


class Client(NamedTuple):
    id: ClientID
    account: AccountID


class Bank:
    """The use cases wired to the real infrastructure, as the drivers do.
    Scenarios are built only through business operations."""

    def __init__(self):
        pool = PostgresqlConnectionPool(psycopg2_create_connection, 1)
        identity = ThreadIdentity()
        self.accounts = accounts = AccountsRepository(pool, identity)
        clients = ClientsRepository(pool, identity)
        self.context = context = DBTransactionContext(pool, identity)

        self.register_client = RegisterClientUseCase(
            clients, context, Password
        )
        self.auth = AuthServiceDB(context, pool, identity)
        self.get_accounts = GetAccountsUseCase(accounts, context)
        self.get_balance = GetBalanceUseCase(accounts, context)
        self.get_transactions = GetTransactionsUseCase(accounts, context)
        self.deposit = DepositUseCase(accounts, context)
        self.transfer = TransferFundsUseCase(accounts, context)
        self.new_bank_account = NewBankAccountUseCase(accounts, context)

        passkeys = PasskeysRepository(pool, identity)
        ceremonies = CeremoniesRepository(pool, identity)
        relying_party = WebAuthnRelyingParty(RP_ID, "Test bank", ORIGIN)
        self.start_registration = StartPasskeyRegistration(
            clients, ceremonies, relying_party, context
        )
        self.finish_registration = FinishPasskeyRegistration(
            clients, passkeys, ceremonies, relying_party, context
        )
        self.start_authentication = StartPasskeyAuthentication(
            passkeys, ceremonies, relying_party, context, b"decoy key"
        )
        self.finish_authentication = FinishPasskeyAuthentication(
            passkeys, ceremonies, relying_party, context
        )

    def open_client(self, login: str) -> Client:
        """A new client, signed up with a passkey as on the web."""
        key = SoftwareAuthenticator(ORIGIN)
        client = self.register_with_passkey(login, key)\
            .or_else_throw(AssertionError(f"{login} could not sign up"))
        [account] = self.get_accounts.execute(client.id)
        return Client(client.id, account)

    def register_with_passkey(self,
                              login: str,
                              authenticator
                              ) -> Maybe[SignedInClient]:
        """What the browser does on the sign-up page."""
        return self.start_registration.execute(login).flat_map(
            lambda ceremony: self.finish_registration.execute(
                ceremony.ceremony_id,
                authenticator.create(ceremony.public_key)
            )
        )

    def sign_in_with_passkey(self,
                             login: str,
                             authenticator
                             ) -> Maybe[SignedInClient]:
        """What the browser does on the sign-in page."""
        return self.start_authentication.execute(login).flat_map(
            lambda ceremony: self.finish_authentication.execute(
                ceremony.ceremony_id,
                authenticator.get(ceremony.public_key)
            )
        )
