from maybe import maybe
from drivers.Web.http_response import httpResponse
from drivers.Web.HttpRequest.httpRequest import httpRequest


class route:
    def __call__(self, request: httpRequest) -> maybe[httpResponse]:
        raise NotImplementedError
