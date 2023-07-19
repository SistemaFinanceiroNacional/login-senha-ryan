from drivers.web.application.controllers.home import HomeHandler
from drivers.web.application.controllers.logged import LoggedHandler
from drivers.web.application.controllers.logout import LogoutHandler
from drivers.web.application.controllers.register_client import (
    RegisterClientHandler
)
from drivers.web.framework.router import Router
from drivers.web.framework.routes import FixedRoute
from drivers.web.framework.httprequest.http_request import HttpRequest
from usecases.unlogged_cases import UnloggedUseCases
from usecases.logged_cases import LoggedUseCases
from infrastructure.authserviceinterface import AuthServiceInterface
import logging

logger = logging.getLogger("drivers.Web.application.bank_application")


class Ui:
    def __init__(self,
                 auth_service: AuthServiceInterface,
                 unlogged_cases: UnloggedUseCases,
                 logged_cases: LoggedUseCases
                 ):
        self.auth_service = auth_service
        self.unlogged_cases = unlogged_cases
        self.logged_cases = logged_cases

    def __call__(self, request: HttpRequest):
        get_accounts = self.logged_cases.get_accounts
        return Router(
            FixedRoute("/", HomeHandler(self.auth_service, get_accounts)),
            FixedRoute("/logout", LogoutHandler()),
            FixedRoute(
                "/register",
                RegisterClientHandler(self.unlogged_cases.register_client)
            ),
            FixedRoute(
                "/selectaccount",
                LoggedHandler(
                    self.logged_cases.get_balance,
                    self.logged_cases.get_transactions
                )
            )
        )(request)
