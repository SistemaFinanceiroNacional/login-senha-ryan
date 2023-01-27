import maybe

class endpointRoute:
    def __init__(self, endpoint, handler):
        self.endpoint = endpoint
        self.handler = handler

    def __call__(self, request):
        if request.getResource().getEndpoint().startswith(self.endpoint):
            return maybe.just(self.handler(request))
        return maybe.nothing()