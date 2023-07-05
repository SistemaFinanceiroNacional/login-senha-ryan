import logging
import maybe
from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.route_interface import Route

logger = logging.getLogger("drivers.Web.router")


class Router:
    def __init__(self, *routes: Route):
        self.routes = routes

    def __call__(self, request: HttpRequest) -> HttpResponse:
        possible_responses = map(
            lambda route_arg: route_arg(request),
            self.routes
        )
        possible_response = maybe.get_first_not_empty(possible_responses)
        logger.info(f"Resource: {request.get_resource()};"
                    f" Method: {request.get_method()}")
        return possible_response.or_else(lambda: HttpResponse({}, "", 404))
