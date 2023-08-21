from maybe import Maybe
from domain.commontypes.types import ClientId


class AuthServiceInterface:
    def authenticate(self, username: str, password: str) -> Maybe[ClientId]:
        raise NotImplementedError
