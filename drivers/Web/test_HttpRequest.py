from drivers.Web import httpRequest
from drivers.Web import IncompleteHttpRequest

import pytest

import logging

from fake_config.fakes import fakeSocket

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.http_request
def test_default_request():
    noTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(noTagsHeader)
    assert len(request.getHeaders()) == 0


@pytest.mark.http_request
def test_host_header():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n'
                               b'Host: www.ryanbanco.com.br\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert len(request.getHeaders()) == 1


@pytest.mark.http_request
def test_host_header_value():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n'
                               b'Host: www.ryanbanco.com.br\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeaders()['Host'] == 'www.ryanbanco.com.br'


@pytest.mark.http_request
def test_2_headers():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n'
                               b'Host: www.ryanbanco.com.br\r\n'
                               b'User-Agent: Mozilla 5.0\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeaders()['User-Agent'] == 'Mozilla 5.0'


@pytest.mark.http_request
def test_3_headers():
    oneTagsHeader = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n'
                               b'Host: www.ryanbanco.com.br\r\n'
                               b'User-Agent: Mozilla 5.0\r\n'
                               b'Accept-Language: en-US\r\n\r\n')
    request = httpRequest.getNextHttpRequest(oneTagsHeader)
    assert request.getHeaders()['Accept-Language'] == 'en-US'


@pytest.mark.http_request
def test_getting_methodGet():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    method, _, _ = httpRequest.getFirstLine(socket)
    assert method == "GET"


@pytest.mark.http_request
def test_getting_methodPost():
    socket = fakeSocket(b'POST /bank/Main-page HTTP/1.1\r\n')
    method, _, _ = httpRequest.getFirstLine(socket)
    assert method == "POST"


@pytest.mark.http_request
def test_resource_getEndpoint():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    _, resource, _ = httpRequest.getFirstLine(socket)
    assert resource.getEndpoint() == "/bank/Main-page"


@pytest.mark.http_request
def test_resource_getQueryParameters():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    _, resource, _ = httpRequest.getFirstLine(socket)
    assert resource.getQueryParameters() == {}


@pytest.mark.http_request
def test_getting_version():
    socket = fakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    _, _, version = httpRequest.getFirstLine(socket)
    assert version == "1.1"


@pytest.mark.http_request
def test_getBody():
    oneTagHeader = {'Content-Length': '20'}
    socket = fakeSocket(b'a' * 20)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b'a'*20


@pytest.mark.http_request
def test_getBody_size_limited():
    oneTagHeader = {'Content-Length': '20'}
    socket = fakeSocket(b'a' * 50)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b'a'*20


@pytest.mark.http_request
def test_getBody_incomplete_request():
    oneTagHeader = {'Content-Length': '20'}
    socket = fakeSocket(b'a' * 15)
    with pytest.raises(IncompleteHttpRequest.IncompleteHttpRequest):
        httpRequest.getBody(socket, oneTagHeader)


@pytest.mark.http_request
def test_getBody_limited_to_zero():
    oneTagHeader = {b'Content-Length': b'0'}
    socket = fakeSocket(b'a' * 15)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b''


@pytest.mark.http_request
def test_getBody_noContentLength():
    oneTagHeader = {}
    socket = fakeSocket(b'a' * 15)
    body = httpRequest.getBody(socket, oneTagHeader)
    assert body == b''


@pytest.mark.http_request_getResource
def test_endpoint():
    socket = fakeSocket(b'GET /bank/main-page?login=ryanbanco&password=abc123'
                        b' HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getEndpoint() == "/bank/main-page"


@pytest.mark.http_request_getResource
def test_queryParameters():
    socket = fakeSocket(b'GET /bank/main-page?login=ryanbanco&password=abc123'
                        b' HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(socket)
    queryParameters = request.getResource().getQueryParameters()
    assert queryParameters == {"login": "ryanbanco", "password": "abc123"}


@pytest.mark.http_request_getResource
def test_NO_queryParameters():
    socket = fakeSocket(b'GET /bank/main-page? HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getQueryParameters() == {}


@pytest.mark.http_request_getResource
def test_NO_queryParameters_no_interrogation_point():
    socket = fakeSocket(b'GET /bank/main-page HTTP/1.1\r\n\r\n')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getQueryParameters() == {}


@pytest.mark.http_request_getBody
def test_getNextHttpRequest_complete():
    socket = fakeSocket(b'POST / HTTP/1.1\r\n'
                        b'Content-Length: 31\r\n'
                        b'\r\nlogin=ryanbanco&password=abc123')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getBody() == b'login=ryanbanco&password=abc123'


@pytest.mark.http_request_getMethod
def test_getNextHttpRequest_complete_2():
    socket = fakeSocket(b'POST / HTTP/1.1\r\n'
                        b'Content-Length: 31\r\n'
                        b'\r\nlogin=ryanbanco&password=abc123')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getMethod() == "POST"


@pytest.mark.http_request_getResource
def test_verifying_endpoint():
    socket = fakeSocket(b'POST / HTTP/1.1\r\nContent-Length: 31\r\n'
                        b'\r\nlogin=ryanbanco&password=abc123')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getEndpoint() == "/"


@pytest.mark.http_request_getResource
def test_empty_queryParameters():
    socket = fakeSocket(b'POST / HTTP/1.1\r\nContent-Length: 31\r\n'
                        b'\r\nlogin=ryanbanco&password=abc123')
    request = httpRequest.getNextHttpRequest(socket)
    assert request.getResource().getQueryParameters() == {}
