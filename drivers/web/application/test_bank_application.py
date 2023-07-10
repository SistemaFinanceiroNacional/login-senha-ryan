import pytest
from typing import Dict
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
from usecases.unlogged_cases import UnloggedUseCases
from usecases.logged_cases import LoggedUseCases
from usecases.transfer import TransferFundsUseCase
from usecases.new_bank_account import NewBankAccountUseCase
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

    transfer_use_case = TransferFundsUseCase(accounts_repo, context)
    get_accounts = GetBalanceUseCase(accounts_repo, context)
    get_balance = GetAccountsUseCase(accounts_repo, context)
    get_transactions = GetTransactionsUseCase(accounts_repo, context)
    new_bank_use_case = NewBankAccountUseCase(accounts_repo, context)
    register_use_case = RegisterClientUseCase(clients_repo, context, Password)

    auth = FakeAuthService({})
    unlogged = UnloggedUseCases(register_use_case)
    logged = LoggedUseCases(transfer_use_case,
                            get_balance,
                            get_accounts,
                            get_transactions,
                            new_bank_use_case
                            )

    configure_template(settings)
    configure_auth_redirect(settings.AUTH_REDIRECT)
    return bank_application.Ui(auth, unlogged, logged)


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
