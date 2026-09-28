import socket
from urllib.parse import urlparse

import pytest

from e2e.conftest import IDLE_TIMEOUT_SECONDS
from e2e.raw_http import exchange, is_serving

pytestmark = pytest.mark.integration

MALFORMED_REQUESTS = {
    "non-numeric Content-Length":
        b"POST /logout HTTP/1.1\r\nHost: x\r\nContent-Length: abc\r\n\r\n",
    "request line that is not UTF-8":
        b"GET /\xff\xfe HTTP/1.1\r\nHost: x\r\n\r\n",
    "header that is not UTF-8":
        b"GET / HTTP/1.1\r\nHost: \xff\xfe\r\n\r\n",
}

HANDLED_REQUESTS = {
    "query parameter without a value":
        b"GET /?debug HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n",
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

    assert status is not None and status < 500
    assert is_serving(base_url)


@pytest.mark.parametrize("request_bytes", MALFORMED_REQUESTS.values(),
                         ids=MALFORMED_REQUESTS.keys())
def test_a_malformed_request_is_answered_and_the_server_survives(
        web_app, request_bytes
):
    assert_answered_and_alive(web_app.base_url, request_bytes)


@pytest.mark.parametrize("request_bytes", HANDLED_REQUESTS.values(),
                         ids=HANDLED_REQUESTS.keys())
def test_odd_but_handled_requests_are_answered(web_app, request_bytes):
    assert_answered_and_alive(web_app.base_url, request_bytes)


def test_a_kept_alive_connection_does_not_block_the_others(web_app):
    address = urlparse(web_app.base_url)
    browser = socket.create_connection((address.hostname, address.port or 80))
    with browser:
        # Like a browser: one request, then the connection is kept open for
        # later ones.
        browser.sendall(b"GET / HTTP/1.1\r\nHost: x\r\n\r\n")
        assert browser.recv(12).startswith(b"HTTP/1.1 200")

        assert is_serving(web_app.base_url)


def test_a_failing_handler_answers_500_and_the_server_survives(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    alice.open_account()

    # A deposit without any body makes the handler fail.
    status = alice.page.evaluate(
        """() => fetch("/deposit", {
            method: "POST",
            headers: {"X-CSRF-Token": document.querySelector(
                'meta[name="csrf-token"]').content},
        }).then(response => response.status)"""
    )

    assert status == 500
    assert is_serving(alice.web_app.base_url)


@pytest.mark.parametrize("request_bytes, expected", [
    (b"POST /logout HTTP/1.1\r\nHost: x\r\n"
     b"Content-Length: 10000000000\r\n\r\n", 413),
    (b"GET /" + b"a" * 16000 + b" HTTP/1.1\r\nHost: x\r\n\r\n", 414),
    (b"GET / HTTP/1.1\r\nHost: x\r\nX-Filler: " + b"a" * 32000 + b"\r\n\r\n",
     431),
], ids=["huge body", "huge request line", "huge headers"])
def test_oversized_requests_are_refused(web_app, request_bytes, expected):
    assert exchange(web_app.base_url, request_bytes) == expected
    assert is_serving(web_app.base_url)


def test_a_negative_content_length_is_refused(web_app):
    assert_answered_and_alive(
        web_app.base_url,
        b"POST /logout HTTP/1.1\r\nHost: x\r\nContent-Length: -1\r\n\r\n"
    )


def test_a_stalled_connection_is_closed(web_app):
    address = urlparse(web_app.base_url)
    stalled = socket.create_connection((address.hostname, address.port or 80))
    with stalled:
        stalled.sendall(b"GET / HTTP/1.1\r\n")
        stalled.settimeout(IDLE_TIMEOUT_SECONDS + 3)
        try:
            closed = stalled.recv(1) == b""
        except OSError:
            closed = False

    assert closed
