import logging
import maybe
from drivers.Web.httpResponse import httpResponse
from drivers.Web.httpRequest import httpRequest
from drivers.Web.routeInterface import route

logger = logging.getLogger("drivers.Web.router")


class router:
    def __init__(self, *routes: route):
        self.routes = routes

    def __call__(self, request: httpRequest) -> httpResponse:
        possible_responses = map(
            lambda route_arg: route_arg(request),
            self.routes
        )
        possible_response = maybe.getFirstNotEmpty(possible_responses)
        logger.info(f"Resource: {request.getResource()};"
                    f" Method: {request.getMethod()}")
        return possible_response.orElse(lambda: httpResponse({}, "", 404))
