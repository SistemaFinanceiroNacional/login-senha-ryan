import pytest
from typing import Dict

from drivers.web.application.controllers.home import HomeHandler
from drivers.web.application.controllers.logged import LoggedHandler
from drivers.web.application.controllers.logout import LogoutHandler
from drivers.web.application.controllers.register_client import (
    RegisterClientHandler
)
from drivers.web.framework.template import configure_template
from drivers.web.application import settings
from drivers.web.framework.httprequest.resource import HttpResource
from drivers.web.framework.httprequest.session import configure_auth_redirect
from drivers.web.framework.httprequest import http_request
from fake_config.fakes import (
    FakeContext,
    ContasFake,
    ClientsFake,
    FakeAuthService
)
from usecases.get_balance import GetBalanceUseCase
from usecases.get_accounts import GetAccountsUseCase
from usecases.register_client import RegisterClientUseCase
from usecases.get_transactions import GetTransactionsUseCase
from drivers.web.application import bank_application
from password import Password


@pytest.fixture
def ui_example():
    accounts_repo = ContasFake({}, {})
    clients_repo = ClientsFake({})
    context = FakeContext()

    get_balance = GetBalanceUseCase(accounts_repo, context)
    get_accounts = GetAccountsUseCase(accounts_repo, context)
    get_transactions = GetTransactionsUseCase(accounts_repo, context)
    register_use_case = RegisterClientUseCase(clients_repo, context, Password)

    auth = FakeAuthService({})

    home_handler = HomeHandler(auth, get_accounts)
    logout_handler = LogoutHandler()
    register_handler = RegisterClientHandler(register_use_case)
    logged_handler = LoggedHandler(get_balance, get_transactions)

    configure_template(settings)
    configure_auth_redirect(settings.AUTH_REDIRECT)
    return bank_application.Ui(home_handler,
                               logout_handler,
                               register_handler,
                               logged_handler
                               )


def test_request_using_users_as_resource_returns_404(ui_example):
    header: Dict[str, str] = {}
    body = b''
    method = "GET"
    resource = HttpResource("/users", {})
    version = "1.1"
    request = http_request.HttpRequest(header, body, method, resource, version)

    bank_application_return = ui_example(request)
    assert bank_application_return.status == 404


def test_request_root_status_is_200(ui_example):
    header: Dict[str, str] = {}
    body = ""
    method = "GET"
    resource = HttpResource("/", {})
    version = "1.1"
    request = http_request.HttpRequest(header, body, method, resource, version)
    bank_application_return = ui_example(request)
    assert bank_application_return.get_status() == 200


def test_request_root_resource_is_html(ui_example):
    header: Dict[str, str] = {}
    body = b''
    method = "GET"
    resource = HttpResource("/", {})
    version = "1.1"
    request = http_request.HttpRequest(header, body, method, resource, version)
    bank_application_return = ui_example(request)
    assert bank_application_return.get_headers()["Content-Type"] == "text/html"


def test_post_status_303(ui_example):
    header: Dict[str, str] = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    resource = HttpResource("/", {})
    method = "POST"
    body = b"login=ryanbanco&password=abc123"
    version = "1.1"
    request = http_request.HttpRequest(header, body, method, resource, version)
    bank_application_return = ui_example(request)
    assert bank_application_return.get_status() == 303
