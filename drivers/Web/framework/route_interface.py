from maybe import Maybe
from drivers.Web.framework.http_response import HttpResponse
from drivers.Web.framework.HttpRequest.httpRequest import HttpRequest


class Route:
    def __call__(self, request: HttpRequest) -> Maybe[HttpResponse]:
        raise NotImplementedError
