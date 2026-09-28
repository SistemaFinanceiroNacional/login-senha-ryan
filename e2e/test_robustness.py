import socket
from urllib.parse import urlparse

import pytest

from e2e.raw_http import exchange, is_serving

pytestmark = pytest.mark.integration

CRASHING_REQUESTS = {
    "non-numeric Content-Length":
        b"POST /logout HTTP/1.1\r\nHost: x\r\nContent-Length: abc\r\n\r\n",
    "request line that is not UTF-8":
        b"GET /\xff\xfe HTTP/1.1\r\nHost: x\r\n\r\n",
    "header that is not UTF-8":
        b"GET / HTTP/1.1\r\nHost: \xff\xfe\r\n\r\n",
    "query parameter without a value":
        b"GET /?debug HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n",
}

HANDLED_REQUESTS = {
    "form field without a value":
        b"POST /passkeys/registration/options HTTP/1.1\r\nHost: x\r\n"
        b"Content-Type: application/x-www-form-urlencoded\r\n"
        b"Content-Length: 3\r\nConnection: close\r\n\r\nfoo",
    "body of an unsupported type":
        b"POST /passkeys/registration/options HTTP/1.1\r\nHost: x\r\n"
        b"Content-Type: application/xml\r\n"
        b"Content-Length: 4\r\nConnection: close\r\n\r\n<x/>",
}


def assert_answered_and_alive(base_url: str, request_bytes: bytes) -> None:
    status = exchange(base_url, request_bytes)

    assert status is not None and 400 <= status < 500
    assert is_serving(base_url)


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="a malformed request kills the server (issue #96)")
@pytest.mark.parametrize("request_bytes", CRASHING_REQUESTS.values(),
                         ids=CRASHING_REQUESTS.keys())
def test_a_malformed_request_is_answered_and_the_server_survives(
        web_app, request_bytes
):
    assert_answered_and_alive(web_app.base_url, request_bytes)


@pytest.mark.parametrize("request_bytes", HANDLED_REQUESTS.values(),
                         ids=HANDLED_REQUESTS.keys())
def test_a_malformed_body_is_refused(web_app, request_bytes):
    assert_answered_and_alive(web_app.base_url, request_bytes)


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="one connection is served at a time (issue #96)")
def test_a_kept_alive_connection_does_not_block_the_others(web_app):
    address = urlparse(web_app.base_url)
    browser = socket.create_connection((address.hostname, address.port or 80))
    with browser:
        # Like a browser: one request, then the connection is kept open for
        # later ones.
        browser.sendall(b"GET / HTTP/1.1\r\nHost: x\r\n\r\n")
        assert browser.recv(12).startswith(b"HTTP/1.1 200")

        assert is_serving(web_app.base_url)
