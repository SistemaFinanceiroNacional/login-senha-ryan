import logging
from typing import Dict

from drivers.web.framework.body import BodyInterface, Body, EmptyBody
from drivers.web.framework.encodings import url_encoded
from drivers.web.framework.httprequest import incomplete_http_request_error
from drivers.web.framework.httprequest.headers import make_headers
from drivers.web.framework.httprequest.resource import make_resource
from drivers.web.framework.httprequest.first_line import get_first_line

logger = logging.getLogger("drivers.Web.HttpRequest.httpRequest")


class HttpRequest:
    headers: Dict[str, str]

    def __init__(self, headers, body, method, resource, version):
        self.headers = headers
        self.body = self._construct_body(body, headers)
        self.method = method
        self.resource = resource
        self.version = version

    def _construct_body(self, body, headers) -> BodyInterface:
        if 'Content-Type' in headers:
            return Body(body, headers['Content-Type'])
        return EmptyBody()

    def get_headers(self) -> Dict[str, str]:
        return self.headers

    def get_body(self) -> BodyInterface:
        return self.body

    def get_method(self):
        return self.method

    def get_resource(self):
        return self.resource

    def get_version(self):
        return self.version


def get_next_http_request(socket):
    method, resource, version = get_first_line(
        socket,
        make_resource,
        url_encoded
    )
    logger.debug(f"Method: {method}; Resource: {resource}; Version: {version}")
    headers = make_headers(socket)
    logger.debug(f"Headers: {headers}")
    body = get_body(socket, headers)
    logger.debug(f"Body: {body.decode('utf-8')}")
    request = HttpRequest(headers, body, method, resource, version)

    return request


def get_body(socket, headers) -> bytes:
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
            raise incomplete_http_request_error.IncompleteHttpRequestError()

        else:
            body += rest
            body_size = len(body)

    return body
