from drivers.web.framework.http_response import (
    HttpResponse,
    template_response
)
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.routes import MethodDispatcher


class RegisterClientHandler(MethodDispatcher):
    """The sign-up page; the registration itself is a passkey ceremony."""

    def get(self, request: HttpRequest) -> HttpResponse:
        return template_response("register.html")
