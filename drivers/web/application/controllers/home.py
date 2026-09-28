from drivers.web.framework.http_response import (
    HttpResponse,
    template_response
)
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.session import (
    auth_needed,
    session_maker
)
from drivers.web.framework.routes import MethodDispatcher
from usecases.get_accounts import GetAccountsUseCase


class HomeHandler(MethodDispatcher):
    """The signed-in client's page; signing in is a passkey ceremony."""

    def __init__(self, get_accounts: GetAccountsUseCase):
        self.get_accounts = get_accounts

    @auth_needed("client_id")
    @auth_needed("login")
    def get(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        client_id = session['client_id']
        accounts = self.get_accounts.execute(client_id)
        context = {"user": session['login'], "accounts": accounts}
        response = template_response("loggedPage.html", context)
        return response
