import json
from threading import get_ident
from typing import Dict, Callable
import logging
from drivers.web.framework.http_response import template_http_response, HttpResponse
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.types import Handler, ThreadId, SessionData

logger = logging.getLogger("drivers.web.framework.httprequest.session")
auth_redirect_template = ""


class Session:
    def __init__(self, session_data: SessionData):
        self.session_data = session_data
        self.valid = True

    def __contains__(self, item: str):
        return item in self.session_data

    def __getitem__(self, key: str):
        return self.session_data[key]

    def __setitem__(self, key, value):
        self.session_data[key] = value

    def invalidate(self):
        self.valid = False

    def to_headers(self):
        date = "Thursday, 1 January 1970 00:00:00 GMT"
        expire = f" Expires={date}" if not self.valid else ""
        user_cookies = json.dumps(self.session_data, separators=(',', ':'))
        cookies = f"loggedUsername={user_cookies};{expire}"
        return {"Set-Cookie": cookies}


sessions: Dict[ThreadId, Session] = {}


def _create_new_session_data(request: HttpRequest) -> SessionData:
    cookies = request.get_headers().get("Cookie", "")
    if "loggedUsername=" not in cookies:
        return {}

    cookie_start_index = cookies.index("loggedUsername=")
    json_start_index = cookie_start_index + len("loggedUsername=")
    json_end_index = cookies[json_start_index:].find(";")
    if json_end_index == -1:
        json_str = cookies[json_start_index:]
    else:
        json_str = cookies[json_start_index:json_end_index + 1]

    session_data = json.loads(json_str)
    return session_data


def session_maker(request: HttpRequest) -> Session:
    global sessions
    if (thread_id := get_ident()) not in sessions:
        logger.debug("Session_maker: Existing Session...")
        logger.debug(f"Session_maker: thread_id = {thread_id}")
        session_data = _create_new_session_data(request)
        sessions[thread_id] = Session(session_data)
    return sessions[thread_id]


def session_middleware(app: Handler) -> Handler:
    global sessions

    def wrapper(request: HttpRequest) -> HttpResponse:
        global sessions
        app_response = app(request)
        if (thread_id := get_ident()) in sessions:
            logger.debug("Middleware: Existing Session...")
            logger.debug(f"Middleware: thread_id 1 = {thread_id}")
            body = app_response.get_body()
            headers = app_response.get_headers()
            status = app_response.get_status()
            session = sessions[thread_id]
            response = HttpResponse({**headers, **session.to_headers()}, body, status)
            del sessions[thread_id]
            return response
        logger.debug(f"Middleware: thread_id 2 = {thread_id}")
        logger.debug("Middleware: There is no existing Session.")
        return app_response

    return wrapper


def configure_auth_redirect(template_name):
    global auth_redirect_template
    auth_redirect_template = template_name
    logger.debug(f"Auth_redirect_template value: {auth_redirect_template}")


def auth_needed(session_need: str):
    def decorator(f: Callable):
        def wrapped(self, request: HttpRequest):
            session = session_maker(request)
            if session_need not in session:
                session.invalidate()
                return template_http_response(auth_redirect_template,
                                              headers=session.to_headers()
                                              )
            return f(self, request)

        return wrapped

    return decorator
