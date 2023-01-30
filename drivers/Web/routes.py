import maybe
from drivers.Web import httpResponse

class endpointRoute:
    def __init__(self, endpoint, handler):
        self.endpoint = endpoint
        self.handler = handler

    def __call__(self, request):
        if request.getResource().getEndpoint().startswith(self.endpoint):
            return maybe.just(self.handler(request))
        return maybe.nothing()


class fixed_route:
    def __init__(self, fixed_url, handler):
        self.fixed_url = fixed_url
        self.handler = handler

    def __call__(self, request):
        if request.getResource().getEndpoint() == self.fixed_url:
            return maybe.just(self.handler(request))
        return maybe.nothing()

class method_dispatcher:
    def __call__(self, request):
        method = request.getMethod().lower()
        attribute = getattr(type(self), method, None)
        class_attribute = getattr(method_dispatcher, method, None)
        if attribute != class_attribute:
            return attribute(request)

        else:
            return httpResponse.httpResponse({"Allow": self.allowed_methods()}, "", 405)

    def allowed_methods(self):
        possible_methods = ["get", "post"]
        allowed_methods_list = []
        for method in possible_methods:
            if getattr(type(self), method) != getattr(method_dispatcher, method):
                allowed_methods_list.append(method.upper())

        return ", ".join(allowed_methods_list)

    def get(self, request):
        pass

    def post(self, request):
        pass

    def head(self, request):
        pass
