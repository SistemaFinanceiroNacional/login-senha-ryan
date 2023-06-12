from threading import current_thread
from Infrastructure.identityinterface import IdentityInterface


class ThreadIdentity(IdentityInterface):
    def value(self) -> int:
        return current_thread().ident
