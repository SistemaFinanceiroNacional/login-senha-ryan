g
import httpRequest, httpResponse

import logging

import httpRequest
import httpResponse

logger = logging.getLogger(__name__)


class httpConnection:
    def __init__(self, socket):
        self.socket = socket

    def process(self, handler):

        while True:
            request = httpRequest.getNextHttpRequest(self.socket)
            response = handler(request)
            self.socket.sendall(httpResponse.responseAsBytes(response))
            if request.getHeaders().get(b'Connection', b'') == "close":
                break
