from maybe import Nothing, Maybe, Just
from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.route_interface import Route


class EndPointRoute(Route):
    def __init__(self, endpoint, handler):
        self.endpoint = endpoint
        self.handler = handler

    def __call__(self, request: HttpRequest) -> Maybe[HttpResponse]:
        if request.get_resource().get_endpoint().startswith(self.endpoint):
            return Just(self.handler(request))
        return Nothing()


class FixedRoute(Route):
    def __init__(self, fixed_url, handler):
        self.fixed_url = fixed_url
        self.handler = handler

    def __call__(self, request: HttpRequest) -> Maybe[HttpResponse]:
        if request.get_resource().get_endpoint() == self.fixed_url:
            return Just(self.handler(request))
        return Nothing()


class MethodDispatcher:
    def __call__(self, request: HttpRequest) -> HttpResponse:
        method = request.get_method().lower()
        attribute = getattr(type(self), method, None)
        class_attribute = getattr(MethodDispatcher, method, None)
        if attribute != class_attribute and attribute is not None:
            return attribute(self, request)

        else:
            return HttpResponse({"Allow": self.allowed_methods()}, "", 405)

    def allowed_methods(self) -> str:
        possible_methods = ["get", "post", "head"]
        allowed_methods_list = []
        for method in possible_methods:
            derived_method = getattr(type(self), method)
            base_method = getattr(MethodDispatcher, method)
            if derived_method != base_method:
                allowed_methods_list.append(method.upper())

        return ", ".join(allowed_methods_list)

    def get(self, request):
        pass

    def post(self, request):
        pass

    def head(self, request):
        pass
