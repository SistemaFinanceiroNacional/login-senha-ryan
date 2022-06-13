import httpRequest

class httpConnection:
    def __init__(self, socket):
        self.socket = socket

    def process(self, handler):

        while True:
            request = httpRequest.httpRequest(self.socket)
            response = handler(request)
            self.socket.sendall(response.asbytes())
            if request.head()["Connection"] == "close":
                break
