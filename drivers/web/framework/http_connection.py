from drivers.web.framework import http_response
from drivers.web.framework.httprequest import (
    http_request
)
from drivers.web.framework.httprequest import incomplete_http_request_error

import logging

logger = logging.getLogger("drivers.Web.httpConnection")


class HttpConnection:
    def __init__(self, socket):
        self.socket = socket

    def process(self, handler):
        while True:
            try:
                request = http_request.get_next_http_request(self.socket)
            except incomplete_http_request_error.IncompleteHttpRequestError:
                break

            logger.info(f"Resource: {request.get_resource()};"
                        f" Method: {request.get_method()}")
            response = handler(request)
            self.socket.sendall(http_response.response_as_bytes(response))
            if request.get_headers().get('Connection', '') == "close":
                break

            elif response.get_headers().get('Connection', '') == "close":
                break

            elif self.socket.fileno() == -1:
                break
