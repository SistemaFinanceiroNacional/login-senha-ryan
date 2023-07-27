from typing import Callable, Dict, Protocol, List
from types import ModuleType

from drivers.web.framework.http_response_interface import HttpResponseInterface
from drivers.web.framework.httprequest.http_request import HttpRequest

Handler = Callable[[HttpRequest], HttpResponseInterface]
SessionData = Dict[str, str]
ThreadId = int
Middleware = Callable[[Handler], Handler]


class SettingsModule(Protocol):
    BASE_DIR: str
    TEMPLATES: str
    AUTH_REDIRECT: str
    MIDDLEWARES: List[Middleware]
    ROOT_URLCONF: ModuleType
