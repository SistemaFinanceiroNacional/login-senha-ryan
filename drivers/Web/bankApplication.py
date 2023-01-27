from drivers.Web import httpResponse, httpRequest

import logging

logger = logging.getLogger("drivers.Web.bankApplication")

def root(request):
    if request.getResource().getEndpoint() == "/":
        if request.getMethod() == "GET":
            with open("drivers/Web/root/index.html") as index:
                htmlContent = index.read()

            response = httpResponse.httpResponse({"Content-Type": "text/html"}, htmlContent, 200)

        elif request.getMethod() == "POST":
            with open("drivers/Web/root/loggedPage.html") as loggedPage:
                htmlContent = loggedPage.read()

            body = request.getBody().decode("utf-8")
            logger.debug(f"Body-Content: {body}")
            queryParameters = httpRequest.makeQueryParameters(body)
            response = httpResponse.httpResponse({"Content-Type": "text/html"}, htmlContent.replace("{user}", queryParameters["login"]), 200)

        else:
            response = httpResponse.httpResponse({"Allow": "GET, POST"}, "", 405)

        return response

    else:
        logger.error(f"Resource: {request.getResource()}; Method: {request.getMethod()}")
        return httpResponse.httpResponse({}, "", 404)