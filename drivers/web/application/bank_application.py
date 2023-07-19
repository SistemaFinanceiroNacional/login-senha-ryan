from drivers.web.application.controllers.home import HomeHandler
from drivers.web.application.controllers.logged import LoggedHandler
from drivers.web.application.controllers.logout import LogoutHandler
from drivers.web.application.controllers.register_client import (
    RegisterClientHandler
)
from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.router import Router
from drivers.web.framework.routes import FixedRoute
from drivers.web.framework.httprequest.http_request import HttpRequest
import logging

logger = logging.getLogger("drivers.Web.application.bank_application")


class Ui:
    def __init__(
            self,
            home_handler: HomeHandler,
            logout_handler: LogoutHandler,
            register_handler: RegisterClientHandler,
            logged_handler: LoggedHandler
    ):
        self.router = Router(
            FixedRoute("/", home_handler),
            FixedRoute("/logout", logout_handler),
            FixedRoute("/register", register_handler),
            FixedRoute("/selectaccount", logged_handler)
        )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.router(request)
