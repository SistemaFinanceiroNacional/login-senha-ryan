from typing import Callable

QueryMaker = Callable[[str], dict[str, str]]


class http_resource:
    def __init__(self, endpoint, queryParameters):
        self.endpoint = endpoint
        self.queryParameters = queryParameters

    def getEndpoint(self):
        return self.endpoint

    def getQueryParameters(self):
        return self.queryParameters


def makeResource(rawResource: str, query_maker: QueryMaker) -> http_resource:
    splitRawResource = rawResource.split("?")
    endpoint = splitRawResource[0]

    if len(splitRawResource) > 1 and splitRawResource[1] != "":
        queryParameters = query_maker(splitRawResource[1])

    else:
        queryParameters = {}

    return http_resource(endpoint, queryParameters)
