import threading


class identity:
    def value(self) -> int:
        raise NotImplementedError()

class thread_identity(identity):
    def value(self) -> int:
        return threading.current_thread().ident