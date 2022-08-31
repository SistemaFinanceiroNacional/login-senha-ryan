from typing import Protocol

class genericCursor(Protocol):
    def execute(self, string: str) -> None:
        pass
