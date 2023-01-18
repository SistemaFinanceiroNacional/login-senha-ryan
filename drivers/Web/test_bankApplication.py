from drivers.Web import httpRequest, bankApplication


def test_request_using_Users_as_resource_returns_404():
    header = {}
    body = ""
    method = "GET"
    resource = "/users"
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = bankApplication.root(request)
    assert bankApplicationReturn.status == 404

def test_request_root_status_is_200():
    header = {}
    body = ""
    method = "GET"
    resource = "/"
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = bankApplication.root(request)
    assert bankApplicationReturn.status == 200


def test_request_root_resource_is_html():
    header = {}
    body = ""
    method = "GET"
    resource = "/"
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = bankApplication.root(request)
    assert bankApplicationReturn.getHeaders()["Content-Type"] == "text/html"