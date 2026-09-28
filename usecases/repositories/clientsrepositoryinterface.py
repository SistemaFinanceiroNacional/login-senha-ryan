from domain.commontypes.types import ClientID
from maybe import Maybe


class ClientsRepositoryInterface:
    def login_taken(self, login: str) -> bool:
        raise NotImplementedError

    def add_passwordless_client(self, login: str) -> Maybe[ClientID]:
        """Creates the client and its first bank account; Nothing when the
        login was taken in the meantime."""
        raise NotImplementedError
