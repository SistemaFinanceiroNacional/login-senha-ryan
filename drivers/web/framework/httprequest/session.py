import logging
import secrets
from http.cookies import CookieError, SimpleCookie
from typing import Any, Callable, Optional

from drivers.web.framework import settings
from drivers.web.framework.http_response import (
    HttpResponse,
    template_response
)
from drivers.web.framework.http_response_interface import HttpResponseInterface
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.sessionstore import (
    SessionData,
    SessionStoreInterface
)
from drivers.web.framework.types import Handler
from maybe import Just, Maybe, Nothing

logger = logging.getLogger("drivers.web.framework.httprequest.session")

COOKIE_NAME = "session"


class Session:
    """The data of the current visitor, kept on the server. The browser only
    holds an opaque, random token."""

    def __init__(self, token: Optional[str], data: SessionData):
        self.token = token
        self.data = dict(data)
        self.changed = False
        self.rotated = False
        self.invalidated = False

    def __contains__(self, item: str):
        return item in self.data

    def __getitem__(self, key: str):
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        self.data[key] = value
        self.changed = True

    def rotate(self):
        """Continues under a new token, e.g. when signing in, so that a token
        known to someone else before is worth nothing afterwards."""
        self.rotated = True
        self.changed = True

    def invalidate(self):
        """Ends the session: its data is gone from the server."""
        self.invalidated = True
        self.data = {}


def session_cookie(token: str) -> str:
    return f"{COOKIE_NAME}={token}; Path=/"


def expired_session_cookie() -> str:
    return f"{COOKIE_NAME}=; Path=/; Max-Age=0"


def session_token(request: HttpRequest) -> Maybe[str]:
    cookies: SimpleCookie = SimpleCookie()
    try:
        cookies.load(request.get_headers().get("Cookie", ""))
    except CookieError:
        return Nothing()
    if COOKIE_NAME not in cookies or not cookies[COOKIE_NAME].value:
        return Nothing()
    return Just(cookies[COOKIE_NAME].value)


class SessionMiddleware:
    def __init__(self, store: SessionStoreInterface):
        self.store = store

    def __call__(self, app: Handler) -> Handler:
        def wrapper(request: HttpRequest) -> HttpResponseInterface:
            session = self._open(request)
            request.session = session
            response = app(request)
            return self._close(session, response)

        return wrapper

    def _open(self, request: HttpRequest) -> Session:
        return session_token(request).flat_map(
            lambda token: self.store.load(token).map(
                lambda data: Session(token, data)
            )
        ).or_else(lambda: Session(None, {}))

    def _close(self,
               session: Session,
               response: HttpResponseInterface
               ) -> HttpResponseInterface:
        cookie = self._persist(session)
        if cookie is None:
            return response
        headers = {**response.get_headers(), "Set-Cookie": cookie}
        return HttpResponse(headers, response.get_body(),
                            response.get_status())

    def _persist(self, session: Session) -> Optional[str]:
        if session.invalidated:
            if session.token is not None:
                self.store.delete(session.token)
            return expired_session_cookie()

        if session.token is not None and not session.rotated:
            # Every request keeps a live session alive (idle timeout).
            self.store.save(session.token, session.data)
            return None

        if not session.changed:
            return None

        if session.token is not None:
            self.store.delete(session.token)
        token = secrets.token_urlsafe(32)
        self.store.save(token, session.data)
        return session_cookie(token)


def session_maker(request: HttpRequest) -> Session:
    if request.session is None:
        request.session = Session(None, {})
    return request.session


def auth_needed(session_need: str):
    def decorator(f: Callable):
        def wrapped(self, request: HttpRequest):
            if session_need not in session_maker(request):
                return template_response(settings.app_settings.AUTH_REDIRECT)
            return f(self, request)

        return wrapped

    return decorator
