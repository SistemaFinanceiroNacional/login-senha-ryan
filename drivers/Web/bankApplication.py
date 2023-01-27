from drivers.Web import httpResponse, httpRequest, template

import logging

logger = logging.getLogger("drivers.Web.bankApplication")

def root(request):
    if request.getResource().getEndpoint() == "/":
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

    else:
        logger.error(f"Resource: {request.getResource()}; Method: {request.getMethod()}")
        return httpResponse.httpResponse({}, "", 404)