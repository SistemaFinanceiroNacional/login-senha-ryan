import threading
from ApplicationService.repositories.identity import identity

class thread_identity(identity):
    def value(self) -> int:
        return threading.current_thread().ident


