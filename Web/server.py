import socket


def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("127.0.0.1", 8080))
    serverSocket.listen()
    clientSocket, addr = serverSocket.accept()

    dataAux = b''

    while True:
        data = clientSocket.recv(1024)
        if not data:
            break

        else:
            dataAux = dataAux + data

    print()
    clientSocket.sendall(dataAux)
    print(data.decode("utf-8"))

    clientSocket.close()
    serverSocket.close()


if __name__ == "__main__":
    main()
