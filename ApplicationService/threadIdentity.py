from threading import current_thread
from ApplicationService.repositories.identity import identity

class thread_identity(identity):
    def value(self) -> int:
        return current_thread().ident


