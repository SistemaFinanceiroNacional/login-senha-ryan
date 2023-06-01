from password import Password as pw


class ClientsRepositoryInterface:
    def add_client(self, login: str, password: pw) -> bool:
        raise NotImplementedError
