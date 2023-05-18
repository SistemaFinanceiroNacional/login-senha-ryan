from password import password as pw
from maybe import maybe
from ApplicationService.client import Client


class ClientsRepositoryInterface:
    def get_by_credentials(self, login: str, password: pw) -> maybe[Client]:
        raise NotImplementedError
