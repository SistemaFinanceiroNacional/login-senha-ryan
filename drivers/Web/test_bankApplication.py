from drivers.Web import httpRequest, bankApplication


def test_request_using_Users_as_resource_returns_404():
    header = {}
    body = b''
    method = "GET"
    resource = httpRequest.http_resource("/users", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = bankApplication.root(request)
    assert bankApplicationReturn.status == 404

def test_request_root_status_is_200():
    header = {}
    body = ""
    method = "GET"
    resource = httpRequest.http_resource("/", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = bankApplication.root(request)
    assert bankApplicationReturn.getStatus() == 200


def test_request_root_resource_is_html():
    header = {}
    body = b''
    method = "GET"
    resource = httpRequest.http_resource("/", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = bankApplication.root(request)
    assert bankApplicationReturn.getHeaders()["Content-Type"] == "text/html"

def test_post_status_200():
    header = {}
    resource = httpRequest.http_resource("/", {})
    method = "POST"
    body = b"login=ryanbanco&password=abc123"
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = bankApplication.root(request)
    assert bankApplicationReturn.getStatus() == 200


if __name__ == "__main__":
    test_post_status_200()