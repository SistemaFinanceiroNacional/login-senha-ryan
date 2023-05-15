from drivers.Web.template import render_template
from drivers.Web.router import router
from drivers.Web.routes import method_dispatcher, fixed_route
from drivers.Web.httpResponse import httpResponse
from drivers.Web.HttpRequest.httpRequest import (
    httpRequest,
    makeQueryParameters
)
from ApplicationService.transferFundsUseCase import transferFundsUseCase
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.openAccountUseCase import openAccountUseCase
import logging

logger = logging.getLogger("drivers.Web.bankApplication")


class home_handler(method_dispatcher):
    def __init__(self, loginCase: loginUseCase):
        self.login_use_case = loginCase

    def get(self, request: httpRequest) -> httpResponse:
        cookie = request.getHeaders().get("Cookie", "")
        if "loggedUsername=" in cookie:
            cookie_start_index = cookie.index("loggedUsername=")
            username_start_index = cookie_start_index + len("loggedUsername=")
            username_end_index = cookie[username_start_index:].find(";")
            if username_end_index == -1:
                username = cookie[username_start_index:]
            else:
                username = cookie[username_start_index:username_end_index + 1]
            html_content = render_template(
                "loggedPage.html",
                {"user": username}
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
        possible_account = self.login_use_case.execute(
            user_login,
            user_password
        )
        return possible_account.map(lambda account: httpResponse(
            {
                "Set-Cookie": f"loggedUsername={account.get_id()}",
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


class open_account_handler(method_dispatcher):
    def __init__(self, use_case: openAccountUseCase):
        self.open_account_use_case = use_case

    def get(self, request: httpRequest) -> httpResponse:
        html_content = render_template("openAccount.html", {})
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
        opened = self.open_account_use_case.execute(new_username, new_password)
        if opened:
            response = httpResponse({"Location": "/"}, "", 303)
        else:
            response = httpResponse({"Location": "/openaccount"}, "", 303)
        return response


class ui:
    def __init__(self,
                 login_use_case: loginUseCase,
                 transfer_use_case: transferFundsUseCase,
                 open_use_case: openAccountUseCase
                 ):
        self.transfer_use_case = transfer_use_case
        self.login_use_case = login_use_case
        self.open_use_case = open_use_case

    def __call__(self, request: httpRequest):
        return router(
            fixed_route("/", home_handler(self.login_use_case)),
            fixed_route("/logout", logged_handler()),
            fixed_route(
                "/openaccount",
                open_account_handler(self.open_use_case)
            ))(request)
