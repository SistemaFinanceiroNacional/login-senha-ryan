import socket
from typing import Optional
from urllib.parse import urlparse

TIMEOUT_SECONDS = 5


def exchange(base_url: str, raw_request: bytes) -> Optional[int]:
    """Sends bytes as they are over TCP, as any client (or attacker) can,
    and returns the status of the response, or None when the connection
    ends without one."""
    address = urlparse(base_url)
    try:
        with socket.create_connection(
            (address.hostname, address.port or 80), timeout=TIMEOUT_SECONDS
        ) as connection:
            connection.sendall(raw_request)
            status_line = connection.makefile("rb").readline()
    except OSError:
        return None
    parts = status_line.split()
    if len(parts) < 2 or not parts[0].startswith(b"HTTP/"):
        return None
    return int(parts[1])


def is_serving(base_url: str) -> bool:
    return exchange(
        base_url, b"GET / HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n"
    ) == 200


class RawResponse:
    def __init__(self, status: int, headers: dict, body: bytes):
        self.status = status
        self.headers = headers
        self.body = body


def fetch(base_url: str, raw_request: bytes) -> RawResponse:
    """Like exchange(), but reads the whole response."""
    address = urlparse(base_url)
    with socket.create_connection(
        (address.hostname, address.port or 80), timeout=TIMEOUT_SECONDS
    ) as connection:
        connection.sendall(raw_request)
        stream = connection.makefile("rb")
        status = int(stream.readline().split()[1])
        headers = {}
        for line in iter(stream.readline, b"\r\n"):
            name, _, value = line.decode().partition(":")
            headers[name.strip().lower()] = value.strip()
        body = stream.read(int(headers.get("content-length", 0)))
    return RawResponse(status, headers, body)
