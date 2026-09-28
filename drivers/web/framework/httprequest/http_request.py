import logging
from typing import Any, Dict

from drivers.web.framework.body import BodyInterface, Body, EmptyBody
from drivers.web.framework.encodings import url_encoded
from drivers.web.framework.httprequest import incomplete_http_request_error
from drivers.web.framework.httprequest.headers import make_headers
from drivers.web.framework.httprequest.headers_map import Headers
from drivers.web.framework.httprequest.http_error import (
    MAX_BODY_BYTES,
    too_large_body
)
from drivers.web.framework.httprequest.resource import make_resource
from drivers.web.framework.httprequest.first_line import get_first_line

logger = logging.getLogger("drivers.Web.HttpRequest.httpRequest")


class HttpRequest:
    headers: Dict[str, str]

    def __init__(self, headers, body, method, resource, version):
        self.headers = Headers(headers)
        self.body = self._construct_body(body, self.headers)
        self.method = method
        self.resource = resource
        self.version = version
        # Set by the session middleware for the duration of the request.
        self.session: Any = None

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
    logger.debug(f"Method: {method}; Version: {version}")
    headers = Headers(make_headers(socket))
    logger.debug(f"Headers: {redacted(headers)}")
    # Bodies are never logged: they carry credentials and personal data.
    body = get_body(socket, headers)
    request = HttpRequest(headers, body, method, resource, version)

    return request


SECRET_HEADERS = {"cookie", "set-cookie", "authorization", "x-csrf-token"}


def redacted(headers: Dict[str, str]) -> Dict[str, str]:
    """Headers fit for logs: values that grant access are hidden."""
    return {name: "<redacted>" if name.lower() in SECRET_HEADERS else value
            for name, value in headers.items()}


def get_body(socket, headers) -> bytes:
    default_length = '0'
    length = int(headers.get('Content-Length', default_length))
    if length > MAX_BODY_BYTES:
        raise too_large_body()
    body = socket.recv(length)
    body_size = len(body)

    while body_size < length:
        difference = length - body_size
        rest = socket.recv(difference)
        if rest == b'':
            raise incomplete_http_request_error.IncompleteHttpRequestError()

        else:
            body += rest
            body_size = len(body)

    return body
