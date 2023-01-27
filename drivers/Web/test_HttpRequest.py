from drivers.Web import httpRequest
from drivers.Web import IncompleteHttpRequest

import pytest

import logging

logging.basicConfig(level=logging.DEBUG)


class fakeSocket:
    def __init__(self, content):
        self.content = content

    def recv(self, bufsize):
        requiredContent = self.content[0:bufsize]
        self.content = self.content[bufsize:]
        return requiredContent


def test_http_request_1():
    noTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(noTagsHeader)
    assert len(request.getHeaders()) == 0

def test_http_request_host():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert len(request.getHeaders()) == 1

def test_http_request_calling_host():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeaders()['Host'] == 'www.ryanbanco.com.br'

def test_http_request_calling_2_headers():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\nUser-Agent: Mozilla 5.0\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeaders()['User-Agent'] == 'Mozilla 5.0'

def test_http_request_calling_3_headers():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\nUser-Agent: Mozilla 5.0\r\nAccept-Language: en-US\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeaders()['Accept-Language'] == 'en-US'

def test_http_request_getFirstLine_methodGet():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    method, _, _ = httpRequest.getFirstLine(socket)
    assert method == "GET"

def test_http_request_getFirstLine_methodPost():
    socket = fakeSocket(b'POST /bank/Main-page HTTP/1.1\r\n')
    method, _, _ = httpRequest.getFirstLine(socket)
    assert method == "POST"

def test_http_request_getFirstLine_resource_getEndpoint():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    _, resource, _ = httpRequest.getFirstLine(socket)
    assert resource.getEndpoint() == "/bank/Main-page"

def test_http_request_getFirstLine_resource_getQueryParameters():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    _, resource, _ = httpRequest.getFirstLine(socket)
    assert resource.getQueryParameters() == {}

def test_http_request_getFirstLine_version():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    _, _, version = httpRequest.getFirstLine(socket)
    assert version == "1.1"

def test_http_request_getBody():
    oneTagHeader = {'Content-Length': '20'}
    socket = fakeSocket(b'a'*20)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b'a'*20

def test_http_request_getBody2():
    oneTagHeader = {'Content-Length': '20'}
    socket = fakeSocket(b'a'*50)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b'a'*20

def test_http_request_getBody3():
    oneTagHeader = {'Content-Length': '20'}
    socket = fakeSocket(b'a'*15)
    with pytest.raises(IncompleteHttpRequest.IncompleteHttpRequest):
        httpRequest.getBody(socket, oneTagHeader)

def test_http_request_getBody4():
    oneTagHeader = {b'Content-Length': b'0'}
    socket = fakeSocket(b'a'*15)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b''

def test_http_request_getBody_noContentLength():
    oneTagHeader = {}
    socket = fakeSocket(b'a'*15)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b''

def test_resource_endpoint():
    socket = fakeSocket(b'GET /bank/main-page?login=ryanbanco&password=abc123 HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getEndpoint() == "/bank/main-page"

def test_resource_queryParameters():
    socket = fakeSocket(b'GET /bank/main-page?login=ryanbanco&password=abc123 HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getQueryParameters() == {"login": "ryanbanco", "password": "abc123"}

def test_resource_NO_queryParameters():
    socket = fakeSocket(b'GET /bank/main-page? HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getQueryParameters() == {}

def test_resource_NO_queryParameters_without_interrogation_point():
    socket = fakeSocket(b'GET /bank/main-page HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getQueryParameters() == {}

def test_fakeSocket_getNextHttpRequest_complete_getBody():
    socket = fakeSocket(b'POST / HTTP/1.1\r\nContent-Length: 31\r\n\r\nlogin=ryanbanco&password=abc123')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getBody() == b'login=ryanbanco&password=abc123'

def test_fakeSocket_getNextHttpRequest_complete_getMethod():
    socket = fakeSocket(b'POST / HTTP/1.1\r\nContent-Length: 31\r\n\r\nlogin=ryanbanco&password=abc123')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getMethod() == "POST"

def test_fakeSocket_getNextHttpRequest_complete_getResource_getEndpoint():
    socket = fakeSocket(b'POST / HTTP/1.1\r\nContent-Length: 31\r\n\r\nlogin=ryanbanco&password=abc123')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getEndpoint() == "/"

def test_fakeSocket_getNextHttpRequest_complete_getResource_getQueryParameters():
    socket = fakeSocket(b'POST / HTTP/1.1\r\nContent-Length: 31\r\n\r\nlogin=ryanbanco&password=abc123')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getQueryParameters() == {}