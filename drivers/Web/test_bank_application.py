import pytest
import drivers.Web.HttpRequest.Headers
import drivers.Web.HttpRequest.Resource
from drivers.Web.HttpRequest import httpRequest
from fake_config.fakes import (
    fake_connection,
    fake_context,
    fake_identity,
    contasFake
)
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.OpenAccountUseCase import OpenAccountUseCase
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from Infrastructure.authServiceDB import AuthServiceDB
from drivers.Web import bank_application
from password import Password


@pytest.fixture
def ui_example():
    accounts_repo = contasFake({}, {})
    context = fake_context()
    conn = fake_connection()
    iden = fake_identity(1)

    transfer_use_case = TransferFundsUseCase(accounts_repo, context)
    open_use_case = OpenAccountUseCase(accounts_repo, context, Password)
    get_accounts = GetBalanceUseCase(accounts_repo, context)
    get_balance = GetAccountsUseCase(accounts_repo, context)

    auth = AuthServiceDB(context, conn, iden)
    unlogged = UnloggedUseCases(open_use_case)
    logged = LoggedUseCases(transfer_use_case, get_balance, get_accounts)

    return bank_application.ui(auth, unlogged, logged)


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
