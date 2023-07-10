from typing import Dict

from drivers.web.framework.httprequest import (
    http_request,
    first_line
)
from drivers.web.framework.encodings import url_encoded
from drivers.web.framework.httprequest import (
    incomplete_http_request_error as ihre,
    resource
)
from fake_config.fakes import FakeSocket
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)


def qmaker():
    return url_encoded


def rmaker():
    return resource.make_resource


@pytest.mark.http_request
def test_default_request():
    no_tags_header = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n\r\n')
    request = http_request.get_next_http_request(no_tags_header)
    assert len(request.get_headers()) == 0


@pytest.mark.http_request
def test_host_header():
    one_tags_header = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n'
                                 b'Host: www.ryanbanco.com.br\r\n\r\n')
    request = http_request.get_next_http_request(one_tags_header)
    assert len(request.get_headers()) == 1


@pytest.mark.http_request
def test_host_header_value():
    one_tags_header = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n'
                                 b'Host: www.ryanbanco.com.br\r\n\r\n')
    request = http_request.get_next_http_request(one_tags_header)
    assert request.get_headers()['Host'] == 'www.ryanbanco.com.br'


@pytest.mark.http_request
def test_2_headers():
    one_tags_header = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n'
                                 b'Host: www.ryanbanco.com.br\r\n'
                                 b'User-Agent: Mozilla 5.0\r\n\r\n')
    request = http_request.get_next_http_request(one_tags_header)
    assert request.get_headers()['User-Agent'] == 'Mozilla 5.0'


@pytest.mark.http_request
def test_3_headers():
    one_tags_header = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n'
                                 b'Host: www.ryanbanco.com.br\r\n'
                                 b'User-Agent: Mozilla 5.0\r\n'
                                 b'Accept-Language: en-US\r\n\r\n')
    request = http_request.get_next_http_request(one_tags_header)
    assert request.get_headers()['Accept-Language'] == 'en-US'


@pytest.mark.http_request
def test_getting_method_get():
    socket = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    q_maker, r_maker = qmaker(), rmaker()
    method, _, _ = first_line.get_first_line(socket, r_maker, q_maker)
    assert method == "GET"


@pytest.mark.http_request
def test_getting_method_post():
    socket = FakeSocket(b'POST /bank/Main-page HTTP/1.1\r\n')
    q_maker, r_maker = qmaker(), rmaker()
    method, _, _ = first_line.get_first_line(socket, r_maker, q_maker)
    assert method == "POST"


@pytest.mark.http_request
def test_resource_get_endpoint():
    socket = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    q_maker, r_maker = qmaker(), rmaker()
    _, h_resource, _ = first_line.get_first_line(socket, r_maker, q_maker)
    assert h_resource.get_endpoint() == "/bank/Main-page"


@pytest.mark.http_request
def test_resource_get_query_parameters():
    socket = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    q_maker, r_maker = qmaker(), rmaker()
    _, h_resource, _ = first_line.get_first_line(socket, r_maker, q_maker)
    assert h_resource.get_query_parameters() == {}


@pytest.mark.http_request
def test_getting_version():
    socket = FakeSocket(b'GET /bank/Main-page HTTP/1.1\r\n')
    q_maker, r_maker = qmaker(), rmaker()
    _, _, version = first_line.get_first_line(socket, r_maker, q_maker)
    assert version == "1.1"


@pytest.mark.http_request
def test_get_body():
    one_tag_header = {'Content-Length': '20'}
    socket = FakeSocket(b'a' * 20)
    body = http_request.get_body(socket, one_tag_header)
    assert body == b'a' * 20


@pytest.mark.http_request
def test_get_body_size_limited():
    one_tag_header = {'Content-Length': '20'}
    socket = FakeSocket(b'a' * 50)
    body = http_request.get_body(socket, one_tag_header)
    assert body == b'a' * 20


@pytest.mark.http_request
def test_get_body_incomplete_request():
    one_tag_header = {'Content-Length': '20'}
    socket = FakeSocket(b'a' * 15)
    with pytest.raises(ihre.IncompleteHttpRequestError):
        http_request.get_body(socket, one_tag_header)


@pytest.mark.http_request
def test_get_body_limited_to_zero():
    one_tag_header = {b'Content-Length': b'0'}
    socket = FakeSocket(b'a' * 15)
    body = http_request.get_body(socket, one_tag_header)
    assert body == b''


@pytest.mark.http_request
def test_get_body_no_content_length():
    one_tag_header: Dict[bytes, bytes] = {}
    socket = FakeSocket(b'a' * 15)
    body = http_request.get_body(socket, one_tag_header)
    assert body == b''


@pytest.mark.http_request_getResource
def test_endpoint():
    socket = FakeSocket(b'GET /bank/main-page?login=ryanbanco&password=abc123'
                        b' HTTP/1.1\r\n\r\n')
    request = http_request.get_next_http_request(socket)
    assert request.get_resource().get_endpoint() == "/bank/main-page"


@pytest.mark.http_request_getResource
def test_query_parameters():
    socket = FakeSocket(b'GET /bank/main-page?login=ryanbanco&password=abc123'
                        b' HTTP/1.1\r\n\r\n')
    request = http_request.get_next_http_request(socket)
    query_parameters = request.get_resource().get_query_parameters()
    assert query_parameters == {"login": "ryanbanco", "password": "abc123"}


@pytest.mark.http_request_getResource
def test_no_query_parameters():
    socket = FakeSocket(b'GET /bank/main-page? HTTP/1.1\r\n\r\n')
    request = http_request.get_next_http_request(socket)
    assert request.get_resource().get_query_parameters() == {}


@pytest.mark.http_request_getResource
def test_no_query_parameters_no_interrogation_point():
    socket = FakeSocket(b'GET /bank/main-page HTTP/1.1\r\n\r\n')
    request = http_request.get_next_http_request(socket)
    assert request.get_resource().get_query_parameters() == {}


@pytest.mark.http_request_getBody
def test_get_next_http_request_complete():
    socket = FakeSocket(b'POST / HTTP/1.1\r\n'
                        b'Content-Length: 31\r\n'
                        b'Content-Type: application/x-www-form-urlencoded\r\n'
                        b'\r\nlogin=ryanbanco&password=abc123')
    request = http_request.get_next_http_request(socket)
    assert request.get_body().raw() == b'login=ryanbanco&password=abc123'


@pytest.mark.http_request_getMethod
def test_get_next_http_request_complete_2():
    socket = FakeSocket(b'POST / HTTP/1.1\r\n'
                        b'Content-Length: 31\r\n'
                        b'\r\nlogin=ryanbanco&password=abc123')
    request = http_request.get_next_http_request(socket)
    assert request.get_method() == "POST"


@pytest.mark.http_request_getResource
def test_verifying_endpoint():
    socket = FakeSocket(b'POST / HTTP/1.1\r\nContent-Length: 31\r\n'
                        b'\r\nlogin=ryanbanco&password=abc123')
    request = http_request.get_next_http_request(socket)
    assert request.get_resource().get_endpoint() == "/"


@pytest.mark.http_request_getResource
def test_empty_query_parameters():
    socket = FakeSocket(b'POST / HTTP/1.1\r\nContent-Length: 31\r\n'
                        b'\r\nlogin=ryanbanco&password=abc123')
    request = http_request.get_next_http_request(socket)
    assert request.get_resource().get_query_parameters() == {}
