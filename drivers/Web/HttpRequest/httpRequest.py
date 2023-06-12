from drivers.Web.HttpRequest import IncompleteHttpRequest
from drivers.Web.HttpRequest.Headers import make_headers
from drivers.Web.HttpRequest.Resource import make_resource
from drivers.Web.HttpRequest.FirstLine import get_first_line
import logging

logger = logging.getLogger("drivers.Web.HttpRequest.httpRequest")


class HttpRequest:
    headers: dict[str, str]

    def __init__(self, header, body, method, resource, version):
        self.headers = header
        self.body = body
        self.method = method
        self.resource = resource
        self.version = version

    def get_headers(self) -> dict[str, str]:
        return self.headers

    def get_body(self):
        return self.body

    def get_method(self):
        return self.method

    def get_resource(self):
        return self.resource

    def get_version(self):
        return self.version


def make_query_parameters(raw_resource: str) -> dict[str, str]:
    logger.debug(f"String: {raw_resource}")
    keys_and_values = raw_resource.split("&")
    query_parameters = {}
    for key_and_value in keys_and_values:
        key, value = key_and_value.split("=")
        query_parameters[key] = value

    return query_parameters


def get_next_http_request(socket):
    method, resource, version = get_first_line(
        socket,
        make_resource,
        make_query_parameters
    )
    logger.debug(f"Method: {method}; Resource: {resource}; Version: {version}")
    headers = make_headers(socket)
    logger.debug(f"Headers: {headers}")
    body = get_body(socket, headers)
    logger.debug(f"Body: {body}")
    request = HttpRequest(headers, body, method, resource, version)

    return request


def get_body(socket, headers):
    default_length = '0'
    length = int(headers.get('Content-Length', default_length))
    body = socket.recv(length)
    body_size = len(body)
    logger.debug(f"GetBody: length = {length}"
                 f" & actual body = {body}"
                 f" & actual body's size = {body_size}"
                 )

    while body_size < length:
        difference = length - body_size
        rest = socket.recv(difference)
        logger.debug(f"GetBody: While statement: actual rest = {rest}"
                     f" & actual difference = {difference}"
                     )
        if rest == b'':
            raise IncompleteHttpRequest.IncompleteHttpRequest()

        else:
            body += rest
            body_size = len(body)

    return body
