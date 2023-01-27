from drivers.Web import httpResponse, httpRequest, template, router, routes

import logging

logger = logging.getLogger("drivers.Web.bankApplication")

def home_handler(request):
    if request.getMethod() == "GET":
        html_content = template.render_template("index.html", {})
        response = httpResponse.httpResponse({"Content-Type": "text/html"}, html_content, 200)

    elif request.getMethod() == "POST":
        body = request.getBody().decode("utf-8")
        logger.debug(f"Body-Content: {body}")
        queryParameters = httpRequest.makeQueryParameters(body)
        html_content = template.render_template("loggedPage.html", {"user": queryParameters["login"]})
        response = httpResponse.httpResponse({"Content-Type": "text/html"}, html_content, 200)

    else:
        response = httpResponse.httpResponse({"Allow": "GET, POST"}, "", 405)

    return response


root = router.router(routes.endpointRoute("/", home_handler))