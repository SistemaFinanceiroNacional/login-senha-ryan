
import pytest
from Web import httpRequest
from Web import IncompleteHttpRequest

import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)
# logging.disable(logging.CRITICAL)
class fakeSocket:
    def __init__(self, content):
        self.content = content

    def recv(self, bufsize, flags=0):
        requiredContent = self.content[0:bufsize]
        self.content = self.content[bufsize:]
        return requiredContent


def test_http_request_1():
    noTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(noTagsHeader)
    assert len(request.getHeader()) == 0

def test_http_request_host():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert len(request.getHeader()) == 1

def test_http_request_calling_host():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeader()[b'Host'] == b'www.ryanbanco.com.br'

def test_http_request_calling_2_headers():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\nUser-Agent: Mozilla 5.0\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeader()[b'User-Agent'] == b'Mozilla 5.0'

def test_http_request_calling_3_headers():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\nHost: www.ryanbanco.com.br\r\nUser-Agent: Mozilla 5.0\r\nAccept-Language: en-US\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeader()[b'Accept-Language'] == b'en-US'

def test_http_request_getFirstLine_methodGet():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    method, _, _ = httpRequest.getFirstLine(socket)
    assert method == "GET"

def test_http_request_getFirstLine_methodPost():
    socket = fakeSocket(b'POST /bank/Main-page HTTP/1.1\r\n')
    method, _, _ = httpRequest.getFirstLine(socket)
    assert method == "POST"

def test_http_request_getFirstLine_resource():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    _, resource, _ = httpRequest.getFirstLine(socket)
    assert resource == "/bank/Main-page"

def test_http_request_getFirstLine_version():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    _, _, version = httpRequest.getFirstLine(socket)
    assert version == "1.1"

def test_http_request_getBody():
    oneTagHeader = {b'Content-length': b'20'}
    socket = fakeSocket(b'a'*20)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b'a'*20

def test_http_request_getBody2():
    oneTagHeader = {b'Content-length': b'20'}
    socket = fakeSocket(b'a'*50)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b'a'*20

def test_http_request_getBody3():
    oneTagHeader = {b'Content-length': b'20'}
    socket = fakeSocket(b'a'*15)
    with pytest.raises(IncompleteHttpRequest.IncompleteHttpRequest) as exc_info:
        httpRequest.getBody(socket, oneTagHeader)

def test_http_request_getBody4():
    oneTagHeader = {b'Content-length': b'0'}
    socket = fakeSocket(b'a'*15)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b''

def test_http_request_getBody_noContentLength():
    oneTagHeader = {}
    socket = fakeSocket(b'a'*15)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b''
