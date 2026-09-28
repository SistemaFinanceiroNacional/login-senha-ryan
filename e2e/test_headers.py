import json
import re

import pytest

from e2e.raw_http import fetch

pytestmark = pytest.mark.integration


def test_header_names_are_case_insensitive(web_app):
    # A client sending lower-case header names (HTTP/2 proxies, many HTTP
    # libraries) gets the sign-in page, its session and its token...
    page = fetch(web_app.base_url,
                 b"GET / HTTP/1.1\r\nhost: x\r\nconnection: close\r\n\r\n")
    session = page.headers["set-cookie"].split(";")[0]
    token = re.search(rb'name="csrf-token" content="([^"]+)"', page.body)
    assert token is not None

    # ...and can then use the API with lower-case header names too.
    body = json.dumps({"login": "alice"}).encode()
    ceremony = fetch(web_app.base_url, b"\r\n".join([
        b"POST /passkeys/registration/options HTTP/1.1",
        b"host: x",
        b"connection: close",
        b"cookie: " + session.encode(),
        b"x-csrf-token: " + token.group(1),
        b"content-type: application/json",
        b"content-length: " + str(len(body)).encode(),
        b"",
        body,
    ]))

    assert ceremony.status == 200
    assert "challenge" in json.loads(ceremony.body)["publicKey"]
