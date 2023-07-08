import json
from typing import Dict, Callable
import logging
from drivers.web.framework.http_response import template_http_response
from drivers.web.framework.httprequest.http_request import HttpRequest


logger = logging.getLogger("drivers.web.framework.httprequest.session")
auth_redirect_template = ""


class Session:
    def __init__(self, session_data: Dict[str, str]):
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


def session_maker(request: HttpRequest) -> Session:
    cookies = request.get_headers().get("Cookie", "")
    if "loggedUsername=" not in cookies:
        return Session({})

    cookie_start_index = cookies.index("loggedUsername=")
    json_start_index = cookie_start_index + len("loggedUsername=")
    json_end_index = cookies[json_start_index:].find(";")
    if json_end_index == -1:
        json_str = cookies[json_start_index:]
    else:
        json_str = cookies[json_start_index:json_end_index + 1]
    session_data = json.loads(json_str)
    return Session(session_data)


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
