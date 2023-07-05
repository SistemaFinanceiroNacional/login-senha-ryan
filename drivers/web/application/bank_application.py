import json
from drivers.web.framework.template import render_template
from drivers.web.framework.router import Router
from drivers.web.framework.routes import MethodDispatcher, FixedRoute
from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.httprequest.http_request import (
    HttpRequest,
    make_query_parameters
)
from drivers.web.framework.httprequest.session import session_maker
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

    def get(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        if "client_id" not in session or "login" not in session:
            html_content = render_template("index.html", {})
            response = HttpResponse(
                {"Content-Type": "text/html"},
                html_content,
                200
            )
            return response

        client_id = session['client_id']
        accounts = self.get_accounts.execute(client_id)
        html_content = render_template(
            "loggedPage.html",
            {
                "user": session['login'],
                "accounts": accounts
            }
        )
        response = HttpResponse(
            {"Content-Type": "text/html"},
            html_content,
            200
        )
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

        new_session_data = possible_client_id.map(user_cookie).or_else({})
        return HttpResponse({"Location": "/", **new_session_data}, "", 303)

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
        html_content = render_template("register.html", {})
        response = HttpResponse(
            {
                "Content-type": "text/html"
            },
            html_content,
            200
        )
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

    def get(self, request: HttpRequest) -> HttpResponse:
        cookies = request.get_headers().get("Cookie", "")
        if "loggedUsername=" in cookies:
            cookie_start = cookies.index("loggedUsername=")
            json_start = cookie_start + len("loggedUsername=")
            json_end = cookies[json_start:].find(";")
            if json_end == -1:
                json_str = cookies[json_start:]
            else:
                json_str = cookies[json_start: json_end + 1]

            session_data = json.loads(json_str)
            account_id = session_data["account_id"]
            balance = self.get_balance.execute(account_id).or_else(lambda: 0)
            transactions_execute = self.get_transactions.execute
            transactions = transactions_execute(account_id)\
                .or_else(lambda: [])

            context = {"balance": balance, "transactions": transactions}
            html_content = render_template("account.html", context)
            response = HttpResponse(
                {"Content-Type": "text/html"},
                html_content,
                200
            )
        else:
            expires_date = "Thursday, 1 January 1970 00:00:00 GMT"
            response = HttpResponse(
                {
                    "Set-Cookie": f"loggedUsername=; Expires {expires_date}",
                    "Location": "/"
                },
                "",
                303
            )

        return response

    def post(self, request: HttpRequest) -> HttpResponse:
        body = request.get_body().decode("utf-8")
        query_parameters = make_query_parameters(body)
        account_id = query_parameters["account_id"]
        cookies = request.get_headers().get("Cookie", "")
        if "loggedUsername=" in cookies:
            cookie_start = cookies.index("loggedUsername=")
            json_start = cookie_start + len("loggedUsername=")
            json_end = cookies[json_start:].find(";")
            if json_end == -1:
                json_str = cookies[json_start:]
            else:
                json_str = cookies[json_start:json_end + 1]

            session_data = json.loads(json_str)
            session_data["account_id"] = account_id

            def user_cookie():
                return json.dumps(session_data, separators=(',', ':'))

            response = HttpResponse(
                {
                    "Set-Cookie": f"loggedUsername={user_cookie()};",
                    "Location": "/selectaccount"
                }, "", 303)
        else:
            expires_date = "Thursday, 1 January 1970 00:00:00 GMT"
            response = HttpResponse(
                {
                    "Set-Cookie": f"loggedUsername=; Expires {expires_date}",
                    "Location": "/"
                },
                "",
                303
            )
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
