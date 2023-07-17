from typing import Callable, Dict

from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.httprequest.http_request import HttpRequest

Handler = Callable[[HttpRequest], HttpResponse]
SessionData = Dict[str, str]
ThreadId = int
