
from drivers.Web import httpRequest, httpResponse

import logging

logger = logging.getLogger("drivers.Web.httpConnection")

class httpConnection:
    def __init__(self, socket):
        self.socket = socket

    def process(self, handler):
        while True:
            request = httpRequest.getNextHttpRequest(self.socket)
            logger.info(f"Resource: {request.getResource()}; Method: {request.getMethod()}")
            response = handler(request)
            self.socket.sendall(httpResponse.responseAsBytes(response))
            if request.getHeaders().get('Connection', '') == "close":
                break

            elif response.getHeaders().get('Connection', '') == "close":
                break

            elif self.socket.fileno() == -1:
                break
