from typing import Optional

from drivers.web.framework import http_response
from drivers.web.framework.httprequest import (
    http_request
)
from drivers.web.framework.httprequest import incomplete_http_request_error
from drivers.web.framework.httprequest.http_error import HttpError

import logging

logger = logging.getLogger("drivers.Web.httpConnection")

CLOSE = {"Connection": "close"}


class HttpConnection:
    def __init__(self, socket):
        self.socket = socket

    def process(self, handler):
        with self.socket:
            try:
                self._serve(handler)
            except OSError:
                # Timed out waiting for the client, or the client went away.
                pass

    def _serve(self, handler):
        while True:
            request = self._next_request()
            if request is None:
                break
            request.client_address = self._peer_address()

            logger.info(f"Resource: {request.get_resource()};"
                        f" Method: {request.get_method()}")
            try:
                response = handler(request)
            except Exception:
                logger.exception("Request failed")
                self._send(http_response.HttpResponse(CLOSE, "", 500))
                break

            self._send(response)
            if self._closes(request, response):
                break

    def _next_request(self) -> Optional[http_request.HttpRequest]:
        """The next request on the connection, or None when the connection
        must end (the client closed it, or its request was refused)."""
        try:
            return http_request.get_next_http_request(self.socket)
        except incomplete_http_request_error.IncompleteHttpRequestError:
            return None
        except HttpError as error:
            logger.info(f"Request refused: {error}")
            self._send(http_response.HttpResponse(CLOSE, "", error.status))
            return None
        except ValueError:
            # Not valid HTTP (bad encoding, bad Content-Length, ...).
            logger.info("Malformed request refused")
            self._send(http_response.HttpResponse(CLOSE, "", 400))
            return None

    def _closes(self, request, response) -> bool:
        return request.get_headers().get('Connection', '') == "close" \
            or response.get_headers().get('Connection', '') == "close" \
            or self.socket.fileno() == -1

    def _peer_address(self) -> Optional[str]:
        try:
            return self.socket.getpeername()[0]
        except OSError:
            return None

    def _send(self, response) -> None:
        self.socket.sendall(http_response.response_as_bytes(response))
