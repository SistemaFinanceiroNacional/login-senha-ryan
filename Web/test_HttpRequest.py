from Web import httpRequest

class fakeSocket:
    def __init__(self, content):
        self.content = content

    def recv(self, bufsize, flags=0):
        requiredContent = self.content[0:bufsize]
        self.content = self.content[bufsize:]
        return requiredContent


def test_http_request_1():
    noTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n\r\n')
    request = httpRequest.httpRequest(noTagsHeader)
    assert len(request.head().keys()) == 0

def test_http_request_host():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\n\r\n')
    request = httpRequest.httpRequest(oneTagsHeader)
    assert len(request.head().keys()) == 1

def test_http_request_calling_host():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\n\r\n')
    request = httpRequest.httpRequest(oneTagsHeader)
    assert request.head()[b'Host'] == b'www.ryanbanco.com.br'
