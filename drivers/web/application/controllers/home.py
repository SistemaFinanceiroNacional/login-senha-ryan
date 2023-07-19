from typing import Dict

from drivers.web.framework.http_response import (
    HttpResponse,
    template_response,
    redirect_response
)
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.session import (
    auth_needed,
    session_maker
)
from drivers.web.framework.routes import MethodDispatcher
from infrastructure.authserviceinterface import AuthServiceInterface
from usecases.get_accounts import GetAccountsUseCase


class HomeHandler(MethodDispatcher):
    def __init__(self,
                 auth_service: AuthServiceInterface,
                 get_accounts: GetAccountsUseCase
                 ):
        self.auth_service = auth_service
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

    def post(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        body: Dict[str, str] = request.get_body().refine()
        login = body["login"]
        password = body["password"]
        self.auth_service.authenticate(login, password).run(
            lambda _: session.__setitem__('login', login)
        ).run(
            lambda client_id: session.__setitem__('client_id', client_id)
        )
        return redirect_response("/")
