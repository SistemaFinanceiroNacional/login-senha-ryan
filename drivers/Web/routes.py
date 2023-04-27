from maybe import nothing, maybe, just
from drivers.Web.httpResponse import httpResponse
from drivers.Web.httpRequest import httpRequest
from drivers.Web.routeInterface import route


class endpointRoute(route):
    def __init__(self, endpoint, handler):
        self.endpoint = endpoint
        self.handler = handler

    def __call__(self, request: httpRequest) -> maybe[httpResponse]:
        if request.getResource().getEndpoint().startswith(self.endpoint):
            return just(self.handler(request))
        return nothing()


class fixed_route(route):
    def __init__(self, fixed_url, handler):
        self.fixed_url = fixed_url
        self.handler = handler

    def __call__(self, request: httpRequest) -> maybe[httpResponse]:
        if request.getResource().getEndpoint() == self.fixed_url:
            return just(self.handler(request))
        return nothing()


class method_dispatcher:
    def __call__(self, request: httpRequest) -> httpResponse:
        method = request.getMethod().lower()
        attribute = getattr(type(self), method, None)
        class_attribute = getattr(method_dispatcher, method, None)
        if attribute != class_attribute:
            return attribute(self, request)

        else:
            return httpResponse({"Allow": self.allowed_methods()}, "", 405)

    def allowed_methods(self) -> str:
        possible_methods = ["get", "post", "head"]
        allowed_methods_list = []
        for method in possible_methods:
            type_1 = getattr(type(self), method)
            type_2 = getattr(method_dispatcher, method)
            if type_1 != type_2:
                allowed_methods_list.append(method.upper())

        return ", ".join(allowed_methods_list)

    def get(self, request):
        pass

    def post(self, request):
        pass

    def head(self, request):
        pass
