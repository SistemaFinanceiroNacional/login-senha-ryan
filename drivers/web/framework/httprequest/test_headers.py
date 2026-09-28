from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.resource import make_resource
from drivers.web.framework.encodings import url_encoded


def test_header_names_are_case_insensitive():
    request = HttpRequest({"content-type": "application/json"}, b"{}",
                          "POST", make_resource("/", url_encoded), "1.1")

    assert request.get_headers().get("Content-Type") == "application/json"
    assert "CONTENT-TYPE" in request.get_headers()
    assert request.get_body().refine() == {}
