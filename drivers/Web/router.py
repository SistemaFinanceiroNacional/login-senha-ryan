import logging
import maybe
from drivers.Web import httpResponse
from drivers.Web.httpRequest import httpRequest

logger = logging.getLogger("drivers.Web.router")

class router:
    def __init__(self, *routes):
        self.routes = routes

    def __call__(self, request: httpRequest):
        possible_responses = map(lambda route: route(request), self.routes)
        possible_response = maybe.getFirstNotEmpty(possible_responses)
        logger.info(f"Resource: {request.getResource()}; Method: {request.getMethod()}")
        return possible_response.orElse(lambda: httpResponse.httpResponse({}, "", 404))
