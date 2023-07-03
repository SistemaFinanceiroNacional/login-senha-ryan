import pytest
from drivers.Web.framework import http_response


@pytest.fixture
def response_example():
    headers = {"Date": "Mon, 23 May 2005 22:38:34 GMT"}
    body = "<?xml version='1.0' encoding='UTF-8'?>"
    status = 200
    return http_response.HttpResponse(headers, body, status)


def test_http_response_status(response_example):
    assert response_example.get_status() == 200


def test_http_response_get_body(response_example):
    body_expected = "<?xml version='1.0' encoding='UTF-8'?>"
    assert response_example.get_body() == body_expected


def test_http_response_response_as_bytes_body(response_example):
    response_as_bytes = http_response.response_as_bytes(response_example)
    body = response_as_bytes.split(b"\r\n\r\n")[1]
    assert body == b"<?xml version='1.0' encoding='UTF-8'?>"


def test_http_response_response_as_bytes_headers(response_example):
    response_as_bytes = http_response.response_as_bytes(response_example)
    headers = response_as_bytes.split(b"\r\n\r\n")[0]
    set_from_header = {*headers.split(b"\r\n")}
    assert set_from_header == {b"HTTP/1.1 200 OK",
                               b"Date: Mon, 23 May 2005 22:38:34 GMT",
                               b"Content-length: 38"
                               }
