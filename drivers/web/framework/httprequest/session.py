import json
from typing import Dict
from drivers.web.framework.httprequest.http_request import HttpRequest


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
