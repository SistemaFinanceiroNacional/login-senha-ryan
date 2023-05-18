import pytest
import drivers.Web.HttpRequest.Headers
import drivers.Web.HttpRequest.Resource
from drivers.Web import bankApplication
from drivers.Web.HttpRequest import httpRequest
from fake_config import fakes
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.transferFundsUseCase import transferFundsUseCase
from ApplicationService.openAccountUseCase import openAccountUseCase
from ApplicationService.client import Client
from password import password


@pytest.fixture
def ui_example():
    ryan_login = "ryan"
    ryan_pw = password("abc123")
    ryan_acc = Client(ryan_login, ryan_pw, [])
    context = fakes.fake_context()
    clients_repo = fakes.clientsFake({ryan_login: ryan_acc})
    accounts_repo = fakes.contasFake({}, {})

    login_use_case = loginUseCase(clients_repo, context, password)
    transfer_use_case = transferFundsUseCase(accounts_repo, context)
    open_use_case = openAccountUseCase(accounts_repo, context, password)

    return bankApplication.ui(login_use_case, transfer_use_case, open_use_case)


def test_request_using_Users_as_resource_returns_404(ui_example):
    header = {}
    body = b''
    method = "GET"
    resource = drivers.Web.HttpRequest.Resource.http_resource("/users", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)

    bankApplicationReturn = ui_example(request)
    assert bankApplicationReturn.status == 404


def test_request_root_status_is_200(ui_example):
    header = {}
    body = ""
    method = "GET"
    resource = drivers.Web.HttpRequest.Resource.http_resource("/", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = ui_example(request)
    assert bankApplicationReturn.getStatus() == 200


def test_request_root_resource_is_html(ui_example):
    header = {}
    body = b''
    method = "GET"
    resource = drivers.Web.HttpRequest.Resource.http_resource("/", {})
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = ui_example(request)
    assert bankApplicationReturn.getHeaders()["Content-Type"] == "text/html"


def test_post_status_303(ui_example):
    header = {}
    resource = drivers.Web.HttpRequest.Resource.http_resource("/", {})
    method = "POST"
    body = b"login=ryanbanco&password=abc123"
    version = "1.1"
    request = httpRequest.httpRequest(header, body, method, resource, version)
    bankApplicationReturn = ui_example(request)
    assert bankApplicationReturn.getStatus() == 303
