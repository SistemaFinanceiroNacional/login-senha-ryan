from maybe import Maybe
from Domain.CommonTypes.types import ClientID


class AuthServiceInterface:
    def authenticate(self, username: str, password: str) -> Maybe[ClientID]:
        raise NotImplementedError
