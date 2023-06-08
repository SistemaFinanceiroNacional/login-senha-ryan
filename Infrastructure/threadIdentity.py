from threading import current_thread
from Infrastructure.identityinterface import identityInterface


class thread_identity(identityInterface):
    def value(self) -> int:
        return current_thread().ident
