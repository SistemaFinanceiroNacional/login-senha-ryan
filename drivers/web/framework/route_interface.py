from maybe import Maybe
from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.httprequest.http_request import HttpRequest


class Route:
    def __call__(self, request: HttpRequest) -> Maybe[HttpResponse]:
        raise NotImplementedError
