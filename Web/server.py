import httpConnection
import bankApplication

import socket
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG)

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("127.0.0.1", 8080))
    serverSocket.listen()
    clientSocket, addr = serverSocket.accept()
    logging.debug(f"Client connected on IP {clientSocket.getpeername()}")

    connection = httpConnection.httpConnection(clientSocket)
    connection.process(bankApplication.root)

    clientSocket.close()
    serverSocket.close()


if __name__ == "__main__":
    main()
