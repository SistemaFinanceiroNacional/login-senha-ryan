from maybe import Maybe
from domain.commontypes.types import ClientID


class AuthServiceInterface:
    def authenticate(self, username: str, password: str) -> Maybe[ClientID]:
        raise NotImplementedError
