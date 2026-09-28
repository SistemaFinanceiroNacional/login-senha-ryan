import pytest
from drivers.web.framework import http_response


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


def test_json_response():
    response = http_response.json_response({"ceremony": "abc"}, 409)

    assert response.get_status() == 409
    assert response.get_headers()["Content-Type"] == \
        "application/json; charset=utf-8"
    assert response.get_body() == '{"ceremony": "abc"}'
    assert http_response.response_as_bytes(response).startswith(
        b"HTTP/1.1 409 Conflict\r\n"
    )


def test_content_length_counts_bytes():
    body = "Você está logado(a)!"
    response = http_response.HttpResponse({}, body, 200)

    raw = http_response.response_as_bytes(response)

    head, sent_body = raw.split(b"\r\n\r\n", 1)
    assert f"Content-length: {len(sent_body)}".encode() in head.split(b"\r\n")
    assert sent_body.decode("utf-8") == body
