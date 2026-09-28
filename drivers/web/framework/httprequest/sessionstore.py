from typing import Any, Dict

from maybe import Maybe

SessionData = Dict[str, Any]


class SessionStoreInterface:
    """Where session data lives on the server, keyed by the opaque token
    the browser holds."""

    def load(self, token: str) -> Maybe[SessionData]:
        """The data of a live (not expired) session."""
        raise NotImplementedError

    def save(self, token: str, data: SessionData) -> None:
        """Creates or replaces the session, extending its idle timeout."""
        raise NotImplementedError

    def delete(self, token: str) -> None:
        raise NotImplementedError
