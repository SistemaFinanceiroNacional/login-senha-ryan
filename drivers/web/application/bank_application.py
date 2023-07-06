from drivers.web.framework.router import Router
from drivers.web.framework.routes import MethodDispatcher, FixedRoute
from drivers.web.framework.http_response import (
    HttpResponse,
    template_http_response
)
from drivers.web.framework.httprequest.http_request import (
    HttpRequest,
    make_query_parameters
)
from drivers.web.framework.httprequest.session import (
    session_maker,
    auth_needed
)
from usecases.unlogged_cases import UnloggedUseCases
from usecases.logged_cases import LoggedUseCases
from usecases.register_client import RegisterClientUseCase
from usecases.get_transactions import GetTransactionsUseCase
from usecases.get_accounts import GetAccountsUseCase
from usecases.get_balance import GetBalanceUseCase
from infrastructure.authserviceinterface import AuthServiceInterface
import logging

logger = logging.getLogger("drivers.Web.application.bank_application")


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
        response = template_http_response("loggedPage.html", context)
        return response

    def post(self, request: HttpRequest) -> HttpResponse:
        body = request.get_body().decode("utf-8")
        logger.debug(f"Body-Content: {body}")
        query_parameters = make_query_parameters(body)
        user_login = query_parameters["login"]
        user_password = query_parameters["password"]
        possible_client_id = self.auth_service.authenticate(
            user_login,
            user_password
        )

        session = session_maker(request)
        session['login'] = user_login

        def user_cookie(client_id):
            session['client_id'] = client_id
            return session.to_headers()

        session_data = possible_client_id.map(user_cookie).or_else(lambda: {})
        return HttpResponse({"Location": "/", **session_data}, "", 303)


class LoggedHandler(MethodDispatcher):
    def post(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        session.invalidate()
        response = HttpResponse(
            {
                **session.to_headers(),
                "Location": "/"
            },
            "",
            303)
        return response


class RegisterClientHandler(MethodDispatcher):
    def __init__(self, register_client_use_case: RegisterClientUseCase):
        self.register_use_case = register_client_use_case

    def get(self, request: HttpRequest) -> HttpResponse:
        response = template_http_response("register.html")
        return response

    def post(self, request: HttpRequest) -> HttpResponse:
        body = request.get_body().decode("utf-8")
        query_parameters = make_query_parameters(body)
        new_username = query_parameters["newUsername"]
        new_password = query_parameters["newPassword"]
        opened = self.register_use_case.execute(new_username, new_password)
        if opened:
            response = HttpResponse({"Location": "/"}, "", 303)
        else:
            response = HttpResponse({"Location": "/register"}, "", 303)

        return response


class AccountHandler(MethodDispatcher):
    def __init__(self,
                 get_balance: GetBalanceUseCase,
                 get_transactions: GetTransactionsUseCase
                 ):
        self.get_balance = get_balance
        self.get_transactions = get_transactions

    @auth_needed("account_id")
    def get(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        account_id = session["account_id"]
        balance = self.get_balance.execute(account_id).or_else(lambda: 0)
        transactions_execute = self.get_transactions.execute
        transactions = transactions_execute(account_id).or_else(lambda: [])

        context = {"balance": balance, "transactions": transactions}
        response = template_http_response("account.html", context)
        return response

    def post(self, request: HttpRequest) -> HttpResponse:
        body = request.get_body().decode("utf-8")
        query_parameters = make_query_parameters(body)
        account_id = query_parameters["account_id"]

        session = session_maker(request)
        session["account_id"] = account_id

        response = HttpResponse(
            {
                **session.to_headers(),
                "Location": "/selectaccount"
            }, "", 303)
        return response


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
            FixedRoute("/logout", LoggedHandler()),
            FixedRoute(
                "/register",
                RegisterClientHandler(self.unlogged_cases.register_client)
            ),
            FixedRoute(
                "/selectaccount",
                AccountHandler(
                    self.logged_cases.get_balance,
                    self.logged_cases.get_transactions
                )
            )
        )(request)
