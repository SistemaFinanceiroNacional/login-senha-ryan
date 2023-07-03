import pytest
from typing import Dict
import drivers.Web.framework.HttpRequest.Headers
import drivers.Web.framework.HttpRequest.Resource
from drivers.Web.framework.HttpRequest import httpRequest
from fake_config.fakes import (
    FakeContext,
    ContasFake,
    ClientsFake,
    FakeAuthService
)
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.newbankaccountusecase import NewBankAccountUseCase
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from ApplicationService.registerclientusecase import RegisterClientUseCase
from ApplicationService.gettransactionsusecase import GetTransactionsUseCase
from drivers.Web.application import bank_application
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

    return bank_application.Ui(auth, unlogged, logged)


def test_request_using_users_as_resource_returns_404(ui_example):
    header: Dict[bytes, bytes] = {}
    body = b''
    method = "GET"
    resource = drivers.Web.framework.HttpRequest.Resource.HttpResource("/users", {})
    version = "1.1"
    request = httpRequest.HttpRequest(header, body, method, resource, version)

    bank_application_return = ui_example(request)
    assert bank_application_return.status == 404


def test_request_root_status_is_200(ui_example):
    header: Dict[bytes, bytes] = {}
    body = ""
    method = "GET"
    resource = drivers.Web.framework.HttpRequest.Resource.HttpResource("/", {})
    version = "1.1"
    request = httpRequest.HttpRequest(header, body, method, resource, version)
    bank_application_return = ui_example(request)
    assert bank_application_return.get_status() == 200


def test_request_root_resource_is_html(ui_example):
    header: Dict[bytes, bytes] = {}
    body = b''
    method = "GET"
    resource = drivers.Web.framework.HttpRequest.Resource.HttpResource("/", {})
    version = "1.1"
    request = httpRequest.HttpRequest(header, body, method, resource, version)
    bank_application_return = ui_example(request)
    assert bank_application_return.get_headers()["Content-Type"] == "text/html"


def test_post_status_303(ui_example):
    header: Dict[bytes, bytes] = {}
    resource = drivers.Web.framework.HttpRequest.Resource.HttpResource("/", {})
    method = "POST"
    body = b"login=ryanbanco&password=abc123"
    version = "1.1"
    request = httpRequest.HttpRequest(header, body, method, resource, version)
    bank_application_return = ui_example(request)
    assert bank_application_return.get_status() == 303
