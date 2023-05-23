import pytest
from drivers.Web import http_response


@pytest.fixture
def responseExample():
    headers = {"Date": "Mon, 23 May 2005 22:38:34 GMT"}
    body = "<?xml version='1.0' encoding='UTF-8'?>"
    status = 200
    return httpResponse.httpResponse(headers, body, status)


def test_httpResponse_1(responseExample):
    assert responseExample.getStatus() == 200


def test_httpResponse_get_body(responseExample):
    body_expected = "<?xml version='1.0' encoding='UTF-8'?>"
    assert responseExample.getBody() == body_expected


def test_httpResponse_responseAsBytes_Body(responseExample):
    responseAsBytes = httpResponse.responseAsBytes(responseExample)
    body = responseAsBytes.split(b"\r\n\r\n")[1]
    assert body == b"<?xml version='1.0' encoding='UTF-8'?>"


def test_httpResponse_responseAsBytes_Headers(responseExample):
    responseAsBytes = httpResponse.responseAsBytes(responseExample)
    headers = responseAsBytes.split(b"\r\n\r\n")[0]
    setFromHeader = {*headers.split(b"\r\n")}
    assert setFromHeader == {b"HTTP/1.1 200 OK",
                             b"Date: Mon, 23 May 2005 22:38:34 GMT",
                             b"Content-length: 38"
                             }
