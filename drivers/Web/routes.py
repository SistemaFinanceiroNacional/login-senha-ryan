import maybe

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
