from threading import get_ident
from Infrastructure.identityinterface import IdentityInterface


class ThreadIdentity(IdentityInterface):
    def value(self) -> int:
        return get_ident()
