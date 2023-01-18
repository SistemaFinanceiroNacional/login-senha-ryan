
from drivers.Web import httpConnection, bankApplication

import socket
import logging

logging.basicConfig(level=logging.DEBUG)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind(("127.0.0.1", 8080))
        serverSocket.listen()
        logging.info("serverSocket listened")
        clientSocket, addr = serverSocket.accept()
        logging.debug(f"Client connected on IP {clientSocket.getpeername()}")
        connection = httpConnection.httpConnection(clientSocket)
        connection.process(bankApplication.root)


if __name__ == "__main__":
    main()
