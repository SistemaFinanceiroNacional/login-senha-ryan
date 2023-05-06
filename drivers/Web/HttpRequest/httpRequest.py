from drivers.Web.HttpRequest import IncompleteHttpRequest
from drivers.Web.HttpRequest.Headers import make_headers
from drivers.Web.HttpRequest.Resource import makeResource
from drivers.Web.HttpRequest.FirstLine import getFirstLine
import logging

logger = logging.getLogger("drivers.Web.HttpRequest.httpRequest")


class httpRequest:
    headers: dict[str, str]

    def __init__(self, header, body, method, resource, version):
        self.headers = header
        self.body = body
        self.method = method
        self.resource = resource
        self.version = version

    def getHeaders(self) -> dict[str, str]:
        return self.headers

    def getBody(self):
        return self.body

    def getMethod(self):
        return self.method

    def getResource(self):
        return self.resource

    def getVersion(self):
        return self.version


def makeQueryParameters(raw_resource: str) -> dict[str, str]:
    logger.debug(f"String: {raw_resource}")
    keysAndValues = raw_resource.split("&")
    queryParameters = {}
    for keyAndValue in keysAndValues:
        key, value = keyAndValue.split("=")
        queryParameters[key] = value

    return queryParameters


def getNextHttpRequest(socket):
    method, resource, version = getFirstLine(
        socket,
        makeResource,
        makeQueryParameters
    )
    logger.debug(f"Method: {method}; Resource: {resource}; Version: {version}")
    headers = make_headers(socket)
    logger.debug(f"Headers: {headers}")
    body = getBody(socket, headers)
    logger.debug(f"Body: {body}")
    request = httpRequest(headers, body, method, resource, version)

    return request


def getBody(socket, headers):
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
