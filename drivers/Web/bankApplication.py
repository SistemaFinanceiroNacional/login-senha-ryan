from drivers.Web import httpResponse, httpRequest, template, router, routes

import logging

logger = logging.getLogger("drivers.Web.bankApplication")

class home_handler(routes.method_dispatcher):
    def get(self, request: httpRequest.httpRequest) -> httpResponse.httpResponse:
        cookie = request.getHeaders().get("Cookie", "")
        if "loggedUsername=" in cookie:
            cookie_start_index = cookie.index("loggedUsername=")
            username_start_index = cookie_start_index + len("loggedUsername=")
            username_end_index = cookie[username_start_index:].find(";")
            if username_end_index == -1:
                username = cookie[username_start_index:]
            else:
                username = cookie[username_start_index:username_end_index+1]
            html_content = template.render_template("loggedPage.html", {"user": username})
            response = httpResponse.httpResponse({"Content-Type": "text/html"}, html_content, 200)

        else:
            html_content = template.render_template("index.html", {})
            response = httpResponse.httpResponse({"Content-Type": "text/html"}, html_content, 200)

        return response

    def post(self, request: httpRequest.httpRequest) -> httpResponse.httpResponse:
        body = request.getBody().decode("utf-8")
        logger.debug(f"Body-Content: {body}")
        queryParameters = httpRequest.makeQueryParameters(body)
        user_login = queryParameters["_login"]
        response = httpResponse.httpResponse({"Set-Cookie": f"loggedUsername={user_login}", "Location": "/"}, "", 303)
        return response


class logged_handler(routes.method_dispatcher):
    def post(self, request: httpRequest.httpRequest) -> httpResponse.httpResponse:
        response = httpResponse.httpResponse({"Set-Cookie": "loggedUsername=; Expires=Thursday, 1 January 1970 00:00:00 GMT", "Location": "/"}, "", 303)
        return response


root = router.router(
    routes.fixed_route("/", home_handler()),
    routes.fixed_route("/logout", logged_handler())
)