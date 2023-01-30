from drivers.Web import httpResponse, httpRequest, template, router, routes

import logging

logger = logging.getLogger("drivers.Web.bankApplication")

class home_handler(routes.method_dispatcher):
    def get(self, request):
        html_content = template.render_template("index.html", {})
        response = httpResponse.httpResponse({"Content-Type": "text/html"}, html_content, 200)
        return response

    def post(self, request):
        body = request.getBody().decode("utf-8")
        logger.debug(f"Body-Content: {body}")
        queryParameters = httpRequest.makeQueryParameters(body)
        html_content = template.render_template("loggedPage.html", {"user": queryParameters["login"]})
        response = httpResponse.httpResponse({"Content-Type": "text/html"}, html_content, 200)
        return response


root = router.router(routes.fixed_route("/", home_handler()))