from drivers.Web import httpResponse
from drivers.Web.HttpRequest import (
    httpRequest,
    IncompleteHttpRequest
)

import logging

logger = logging.getLogger("drivers.Web.httpConnection")


class httpConnection:
    def __init__(self, socket):
        self.socket = socket

    def process(self, handler):
        while True:
            try:
                request = httpRequest.getNextHttpRequest(self.socket)
            except IncompleteHttpRequest.IncompleteHttpRequest:
                break

            logger.info(f"Resource: {request.getResource()};"
                        f" Method: {request.getMethod()}")
            response = handler(request)
            self.socket.sendall(httpResponse.responseAsBytes(response))
            if request.getHeaders().get('Connection', '') == "close":
                break

            elif response.getHeaders().get('Connection', '') == "close":
                break

            elif self.socket.fileno() == -1:
                break
