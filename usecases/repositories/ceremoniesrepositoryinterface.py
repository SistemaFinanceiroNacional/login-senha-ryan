from maybe import Maybe
from usecases.passkeys.ceremony import Ceremony, CeremonyKind


class CeremoniesRepositoryInterface:
    def start(self, ceremony: Ceremony) -> None:
        raise NotImplementedError

    def consume(self, ceremony_id: str, kind: CeremonyKind) -> Maybe[Ceremony]:
        """Removes and returns the ceremony if it exists, is of that kind
        and has not expired: a challenge is only ever used once."""
        raise NotImplementedError
