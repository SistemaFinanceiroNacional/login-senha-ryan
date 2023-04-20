import logging
from drivers.Web.template import render_template
from drivers.Web.router import router
from drivers.Web.routes import method_dispatcher, fixed_route
from drivers.Web.httpResponse import httpResponse
from drivers.Web.httpRequest import httpRequest, makeQueryParameters
from ApplicationService.transferFundsBetweenAccountsUseCase import transferFundsBetweenAccountsUseCase
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.openAccountUseCase import openAccountUseCase
from password import password

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
            html_content = render_template("loggedPage.html", {"user": username})
            response = httpResponse({"Content-Type": "text/html"}, html_content, 200)

        else:
            html_content = render_template("index.html", {})
            response = httpResponse({"Content-Type": "text/html"}, html_content, 200)

        return response

    def post(self, request: httpRequest) -> httpResponse:
        body = request.getBody().decode("utf-8")
        logger.debug(f"Body-Content: {body}")
        queryParameters = makeQueryParameters(body)
        user_login = queryParameters["login"]
        user_password = password(queryParameters["password"])
        possible_account = self.login_use_case.execute(user_login, user_password)
        return possible_account \
            .map(lambda account: httpResponse({"Set-Cookie": f"loggedUsername={account.get_login()}",
                                               "Location": "/"}, "", 303)) \
            .orElse(lambda: httpResponse({"Location": "/"}, "", 303))


class logged_handler(method_dispatcher):
    def post(self, request: httpRequest) -> httpResponse:
        response = httpResponse(
            {"Set-Cookie": "loggedUsername=; Expires=Thursday, 1 January 1970 00:00:00 GMT", "Location": "/"}, "", 303)
        return response

class open_account_handler(method_dispatcher):
    def post(self, request: httpRequest) -> httpResponse:
        pass

class ui:
    def __init__(self, login_use_case: loginUseCase,
                 transfer_use_case: transferFundsBetweenAccountsUseCase, open_use_case: openAccountUseCase):
        self.transfer_use_case = transfer_use_case
        self.login_use_case = login_use_case
        self.open_use_case = open_use_case

    def __call__(self, request: httpRequest):
        return router(
            fixed_route("/", home_handler()),
            fixed_route("/logout", logged_handler()),
            fixed_route("/openAccount", open_account_handler())
        )(request)
