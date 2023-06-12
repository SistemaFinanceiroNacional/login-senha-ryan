from drivers.Web import http_response
from drivers.Web.HttpRequest import (
    httpRequest,
    IncompleteHttpRequest
)

import logging

logger = logging.getLogger("drivers.Web.httpConnection")


class HttpConnection:
    def __init__(self, socket):
        self.socket = socket

    def process(self, handler):
        while True:
            try:
                request = httpRequest.get_next_http_request(self.socket)
            except IncompleteHttpRequest.IncompleteHttpRequest:
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
