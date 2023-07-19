from drivers.web.framework.http_response import HttpResponse, redirect_response
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.session import session_maker
from drivers.web.framework.routes import MethodDispatcher


class LogoutHandler(MethodDispatcher):
    def post(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        session.invalidate()
        return redirect_response("/")
