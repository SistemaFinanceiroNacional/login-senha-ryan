from maybe import maybe

ClientID = int

class authServiceInterface:
    def authenticate(self, username: str, password: str) -> maybe[ClientID]:
        raise NotImplementedError