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

def test_http_request_calling_2_headers():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\nUser-Agent: Mozilla 5.0\r\n\r\n')
    request = httpRequest.httpRequest(oneTagsHeader)
    assert request.head()[b'User-Agent'] == b'Mozilla 5.0'

def test_http_request_calling_3_headers():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\nUser-Agent: Mozilla 5.0\r\nAccept-Language: en-US\r\n\r\n')
    request = httpRequest.httpRequest(oneTagsHeader)
    assert request.head()[b'Accept-Language'] == b'en-US'

def test_http_request_double_head_call():
    oneTagsHeader = fakeSocket(
        b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\nUser-Agent: Mozilla 5.0\r\nAccept-Language: en-US\r\n\r\n')
    request = httpRequest.httpRequest(oneTagsHeader)
    request2 = httpRequest.httpRequest(oneTagsHeader)

    head1 = request.head()
    head2 = request2.head()
    assert head1 == head2