
import httpConnection
import bankApplication

import socket
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG)

logging.basicConfig(filename='server.log', level=logging.DEBUG)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind(("127.0.0.1", 8080))
        serverSocket.listen()
        with serverSocket.accept() as connectionSocket:
            clientSocket, addr = connectionSocket
            logging.debug(f"Client connected on IP {clientSocket.getpeername()}")

            connection = httpConnection.httpConnection(clientSocket)
            connection.process(bankApplication.root)


if __name__ == "__main__":
    main()
