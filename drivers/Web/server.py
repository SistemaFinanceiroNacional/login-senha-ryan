import logging
import socket
import threading
from drivers.Web import httpConnection

logger = logging.getLogger("drivers.Web.server")


def main(app):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind(("127.0.0.1", 8080))
        serverSocket.listen()
        logger.info("serverSocket listened")
        while True:
            clientSocket, addr = serverSocket.accept()
            logger.debug(f"Client-IP {clientSocket.getpeername()}")
            connection = httpConnection.httpConnection(clientSocket)
            threading.Thread(target=connection.process, args=(app,)).run()
