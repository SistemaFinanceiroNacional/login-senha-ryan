from typing import List

from domain.commontypes.types import ClientID
from domain.passkey import Passkey
from maybe import Maybe


class PasskeysRepositoryInterface:
    def add(self, client_id: ClientID, passkey: Passkey) -> None:
        raise NotImplementedError

    def of_login(self, login: str) -> List[Passkey]:
        raise NotImplementedError

    def find(self,
             login: str,
             credential_id: bytes
             ) -> Maybe[tuple[ClientID, Passkey]]:
        """The passkey with that credential id, only if it belongs to the
        client with that login."""
        raise NotImplementedError

    def update(self, passkey: Passkey) -> None:
        raise NotImplementedError
