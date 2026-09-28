import hmac
import secrets
from contextvars import ContextVar
from typing import Optional

from drivers.web.framework.body import FORM
from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.http_response_interface import HttpResponseInterface
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.session import Session, session_maker
from drivers.web.framework.types import Handler

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
SESSION_KEY = "csrf_token"
FORM_FIELD = "csrf_token"
HEADER = "X-CSRF-Token"

_current_session: ContextVar[Optional[Session]] = ContextVar(
    "current_session", default=None
)


def csrf_token() -> str:
    """The anti-CSRF token of the current session, created on first use.
    Templates put it in forms (hidden field) and pages (meta tag)."""
    session = _current_session.get()
    if session is None:
        return ""
    if SESSION_KEY not in session:
        session[SESSION_KEY] = secrets.token_urlsafe(32)
    return session[SESSION_KEY]


def _submitted_token(request: HttpRequest) -> Optional[str]:
    header = request.get_headers().get(HEADER)
    if header:
        return header
    content_type = request.get_headers().get("Content-Type", "")
    if content_type.split(";")[0].strip().lower() != FORM:
        return None
    try:
        return request.get_body().refine().get(FORM_FIELD)
    except ValueError:
        return None


def _is_valid(request: HttpRequest, session: Session) -> bool:
    expected = session.data.get(SESSION_KEY)
    submitted = _submitted_token(request)
    return bool(expected) and bool(submitted) and \
        hmac.compare_digest(str(expected), str(submitted))


class CsrfMiddleware:
    """Refuses (403) every state-changing request that does not carry the
    anti-CSRF token of its session: a page on another site can make the
    browser send a request, but cannot read the token."""

    def __call__(self, app: Handler) -> Handler:
        def wrapper(request: HttpRequest) -> HttpResponseInterface:
            session = session_maker(request)
            previous = _current_session.set(session)
            try:
                unsafe = request.get_method().upper() not in SAFE_METHODS
                if unsafe and not _is_valid(request, session):
                    return HttpResponse({}, "Forbidden", 403)
                return app(request)
            finally:
                _current_session.reset(previous)

        return wrapper
