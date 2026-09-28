from drivers.web.framework import http_response
from drivers.web.framework.httprequest import (
    http_request
)
from drivers.web.framework.httprequest import incomplete_http_request_error

import logging

logger = logging.getLogger("drivers.Web.httpConnection")

CLOSE = {"Connection": "close"}


class HttpConnection:
    def __init__(self, socket):
        self.socket = socket

    def process(self, handler):
        with self.socket:
            self._serve(handler)

    def _serve(self, handler):
        while True:
            try:
                request = http_request.get_next_http_request(self.socket)
            except incomplete_http_request_error.IncompleteHttpRequestError:
                break
            except ValueError:
                # Not valid HTTP (bad encoding, bad Content-Length, ...).
                logger.info("Malformed request refused")
                self._send(http_response.HttpResponse(CLOSE, "", 400))
                break

            logger.info(f"Resource: {request.get_resource()};"
                        f" Method: {request.get_method()}")
            try:
                response = handler(request)
            except Exception:
                logger.exception("Request failed")
                self._send(http_response.HttpResponse(CLOSE, "", 500))
                break

            self._send(response)
            if request.get_headers().get('Connection', '') == "close":
                break

            elif response.get_headers().get('Connection', '') == "close":
                break

            elif self.socket.fileno() == -1:
                break

    def _send(self, response) -> None:
        self.socket.sendall(http_response.response_as_bytes(response))
