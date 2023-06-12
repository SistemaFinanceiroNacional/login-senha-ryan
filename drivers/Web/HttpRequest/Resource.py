from typing import Callable

QueryMaker = Callable[[str], dict[str, str]]


class HttpResource:
    def __init__(self, endpoint, query_parameters):
        self.endpoint = endpoint
        self.queryParameters = query_parameters

    def get_endpoint(self):
        return self.endpoint

    def get_query_parameters(self):
        return self.queryParameters


def make_resource(raw_resource: str, query_maker: QueryMaker) -> HttpResource:
    split_raw_resource = raw_resource.split("?")
    endpoint = split_raw_resource[0]

    if len(split_raw_resource) > 1 and split_raw_resource[1] != "":
        query_parameters = query_maker(split_raw_resource[1])

    else:
        query_parameters = {}

    return HttpResource(endpoint, query_parameters)
