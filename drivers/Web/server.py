import logging
import socket
import threading
from drivers.Web.framework import http_connection

logger = logging.getLogger("drivers.Web.server")


def main(app):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 8080))
        server_socket.listen()
        logger.info("server_socket listened")
        while True:
            client_socket, addr = server_socket.accept()
            logger.debug(f"Client-IP {client_socket.getpeername()}")
            connection = http_connection.HttpConnection(client_socket)
            threading.Thread(target=connection.process, args=(app,)).run()
