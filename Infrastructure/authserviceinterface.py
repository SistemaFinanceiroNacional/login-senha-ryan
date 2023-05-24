from maybe import maybe

ClientID = int

class AuthServiceInterface:
    def authenticate(self, username: str, password: str) -> maybe[ClientID]:
        raise NotImplementedError