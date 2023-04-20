import pytest

from drivers.Web import httpRequest, bankApplication
from fake_config import fakes
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.transferFundsBetweenAccountsUseCase import transferFundsBetweenAccountsUseCase
from ApplicationService.openAccountUseCase import openAccountUseCase


@pytest.fixture
def ui_example():
    context = fakes.fake_context()
    intRepository = fakes.contasFake({"ryanbanco": ["abc123", 300]}, {})
    extRepository = fakes.fakeExternalRepository()

    login_use_case = loginUseCase(intRepository, context)
    transfer_use_case = transferFundsBetweenAccountsUseCase(intRepository, extRepository, context)
    open_use_case = openAccountUseCase(intRepository, context)

    return bankApplication.ui(login_use_case, transfer_use_case, open_use_case)


def test_request_using_Users_as_resource_returns_404(ui_example):
    header = {}
    body = b''
    method = "GET"
    resource = httpRequest.http_resource("/users", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)

    bankApplicationReturn = ui_example(request)
    assert bankApplicationReturn.status == 404


def test_request_root_status_is_200(ui_example):
    header = {}
    body = ""
    method = "GET"
    resource = httpRequest.http_resource("/", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = ui_example(request)
    assert bankApplicationReturn.getStatus() == 200


def test_request_root_resource_is_html(ui_example):
    header = {}
    body = b''
    method = "GET"
    resource = httpRequest.http_resource("/", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = ui_example(request)
    assert bankApplicationReturn.getHeaders()["Content-Type"] == "text/html"


def test_post_status_303(ui_example):
    header = {}
    resource = httpRequest.http_resource("/", {})
    method = "POST"
    body = b"login=ryanbanco&password=abc123"
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = ui_example(request)
    assert bankApplicationReturn.getStatus() == 303
