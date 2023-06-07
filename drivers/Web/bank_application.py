import json
from drivers.Web.template import render_template
from drivers.Web.router import router
from drivers.Web.routes import method_dispatcher, fixed_route
from drivers.Web.http_response import httpResponse
from drivers.Web.HttpRequest.httpRequest import (
    httpRequest,
    makeQueryParameters
)
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.registerclientusecase import RegisterClientUseCase
from ApplicationService.gettransactionsusecase import GetTransactionsUseCase
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from Infrastructure.authserviceinterface import AuthServiceInterface
import logging

logger = logging.getLogger("drivers.Web.bankApplication")


class home_handler(method_dispatcher):
    def __init__(self,
                 auth_service: AuthServiceInterface,
                 get_accounts: GetAccountsUseCase
                 ):
        self.auth_service = auth_service
        self.get_accounts = get_accounts

    def get(self, request: httpRequest) -> httpResponse:
        cookie = request.getHeaders().get("Cookie", "")
        if "loggedUsername=" in cookie:
            cookie_start_index = cookie.index("loggedUsername=")
            json_start_index = cookie_start_index + len("loggedUsername=")
            json_end_index = cookie[json_start_index:].find(";")
            if json_end_index == -1:
                json_str = cookie[json_start_index:]
            else:
                json_str = cookie[json_start_index:json_end_index + 1]

            session_data = json.loads(json_str)
            client_id = session_data['client_id']
            accounts = self.get_accounts.execute(client_id)
            html_content = render_template(
                "loggedPage.html",
                {
                    "user": session_data['login'],
                    "accounts": accounts
                }
            )
            response = httpResponse(
                {"Content-Type": "text/html"},
                html_content,
                200
            )
        else:
            html_content = render_template("index.html", {})
            response = httpResponse(
                {"Content-Type": "text/html"},
                html_content,
                200
            )

        return response

    def post(self, request: httpRequest) -> httpResponse:
        body = request.getBody().decode("utf-8")
        logger.debug(f"Body-Content: {body}")
        queryParameters = makeQueryParameters(body)
        user_login = queryParameters["login"]
        user_password = queryParameters["password"]
        possible_client_id = self.auth_service.authenticate(
            user_login,
            user_password
        )

        def user_cookie(client_id):
            session_data = {'login': user_login, 'client_id': client_id}
            return json.dumps(session_data, separators=(',', ':'))

        return possible_client_id.map(lambda client_id: httpResponse(
            {
                "Set-Cookie": f"loggedUsername={user_cookie(client_id)}",
                "Location": "/"
            },
            "",
            303
        )).orElse(
            lambda: httpResponse(
                {"Location": "/"},
                "",
                303
            ))


class logged_handler(method_dispatcher):
    def post(self, request: httpRequest) -> httpResponse:
        expires_date = "Thursday, 1 January 1970 00:00:00 GMT"
        response = httpResponse(
            {
                "Set-Cookie": f"loggedUsername=; Expires={expires_date}",
                "Location": "/"
            },
            "",
            303)
        return response


class register_client_handler(method_dispatcher):
    def __init__(self, register_client_use_case: RegisterClientUseCase):
        self.register_use_case = register_client_use_case

    def get(self, request: httpRequest) -> httpResponse:
        html_content = render_template("register.html", {})
        response = httpResponse(
            {
                "Content-type": "text/html"
            },
            html_content,
            200
        )
        return response

    def post(self, request: httpRequest) -> httpResponse:
        body = request.getBody().decode("utf-8")
        queryParameters = makeQueryParameters(body)
        new_username = queryParameters["newUsername"]
        new_password = queryParameters["newPassword"]
        opened = self.register_use_case.execute(new_username, new_password)
        if opened:
            response = httpResponse({"Location": "/"}, "", 303)
        else:
            response = httpResponse({"Location": "/register"}, "", 303)

        return response


class account_handler(method_dispatcher):
    def __init__(self,
                 get_balance: GetBalanceUseCase,
                 get_transactions: GetTransactionsUseCase
                 ):
        self.get_balance = get_balance
        self.get_transactions = get_transactions

    def get(self, request: httpRequest) -> httpResponse:
        cookies = request.getHeaders().get("Cookie", "")
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
            balance = self.get_balance.execute(account_id)
            transactions = self.get_transactions.execute(account_id)

            context = {"balance": balance, "transactions": transactions}
            html_content = render_template("account.html", context)
            response = httpResponse(
                {"Content-Type": "text/html"},
                html_content,
                200
            )
        else:
            expires_date = "Thursday, 1 January 1970 00:00:00 GMT"
            response = httpResponse(
                {
                    "Set-Cookie": f"loggedUsername=; Expires {expires_date}",
                    "Location": "/"
                },
                "",
                303
            )

        return response

    def post(self, request: httpRequest) -> httpResponse:
        body = request.getBody().decode("utf-8")
        query_parameters = makeQueryParameters(body)
        account_id = query_parameters["account_id"]
        cookies = request.getHeaders().get("Cookie", "")
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

            response = httpResponse(
                {
                    "Set-Cookie": f"loggedUsername={user_cookie()};",
                    "Location": "/selectaccount"
                }, "", 303)
        else:
            expires_date = "Thursday, 1 January 1970 00:00:00 GMT"
            response = httpResponse(
                {
                    "Set-Cookie": f"loggedUsername=; Expires {expires_date}",
                    "Location": "/"
                },
                "",
                303
            )
        return response


class ui:
    def __init__(self,
                 auth_service: AuthServiceInterface,
                 unlogged_cases: UnloggedUseCases,
                 logged_cases: LoggedUseCases
                 ):
        self.auth_service = auth_service
        self.unlogged_cases = unlogged_cases
        self.logged_cases = logged_cases

    def __call__(self, request: httpRequest):
        get_accounts = self.logged_cases.get_accounts
        return router(
            fixed_route("/", home_handler(self.auth_service, get_accounts)),
            fixed_route("/logout", logged_handler()),
            fixed_route(
                "/register",
                register_client_handler(self.unlogged_cases.register_client)
            ),
            fixed_route(
                "/selectaccount",
                account_handler(
                    self.logged_cases.get_balance,
                    self.logged_cases.get_transactions
                )
            )
        )(request)
