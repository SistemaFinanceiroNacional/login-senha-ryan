from maybe import maybe
from Domain.CommonTypes.types import ClientID


class AuthServiceInterface:
    def authenticate(self, username: str, password: str) -> maybe[ClientID]:
        raise NotImplementedError
