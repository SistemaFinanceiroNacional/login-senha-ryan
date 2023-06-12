from password import Password


class ClientsRepositoryInterface:
    def add_client(self, login: str, password: Password) -> bool:
        raise NotImplementedError
