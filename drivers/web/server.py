import logging
import os
import socket
import threading
from drivers.web.framework import http_connection

logger = logging.getLogger("drivers.Web.server")


def idle_timeout_seconds() -> float:
    return float(os.getenv("HTTP_IDLE_TIMEOUT_SECONDS", "30"))


def main(app):
    idle_timeout = idle_timeout_seconds()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 8080))
        server_socket.listen()
        logger.info("server_socket listened")
        while True:
            client_socket, addr = server_socket.accept()
            # A client silent for this long (mid-request or between
            # requests on a kept-alive connection) is disconnected.
            client_socket.settimeout(idle_timeout)
            logger.debug(f"Client-IP {client_socket.getpeername()}")
            connection = http_connection.HttpConnection(client_socket)
            # Each connection in its own thread: a slow or idle client
            # (e.g. a browser keeping its connection alive) must not keep
            # everybody else waiting.
            threading.Thread(
                target=connection.process, args=(app,), daemon=True
            ).start()
