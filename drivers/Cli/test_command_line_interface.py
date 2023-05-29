from drivers.Cli import command_line_interface
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.openAccountUseCase import OpenAccountUseCase
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from Domain.account import Account
from fake_config.fakes import (
    inputfake,
    existing_pedros_account,
    waiting_pedro_account,
    fake_context,
    contasFake,
    fake_authService
)
from password import Password


def test_main_login_and_balance():
    context = fake_context()
    joao_login = "joao"
    joao_pw = Password("ab123")
    joao_acc = Account(1, [])
    a = contasFake({1: [joao_acc]}, {})

    auth_service = fake_authService()
    auth_service.accounts[joao_login] = (joao_pw, 1)

    transferCase = TransferFundsUseCase(a, context)
    openCase = OpenAccountUseCase(a, context, Password)
    get_balance_case = GetBalanceUseCase(a, context)
    get_accounts_case = GetAccountsUseCase(a, context)

    logged_cases = LoggedUseCases(
        transferCase,
        get_accounts_case,
        get_balance_case
    )
    unlogged_cases = UnloggedUseCases(openCase)

    i = inputfake(["3", "2", "3", "1", "1", "1", "abc123", "joao", "1"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[2] == "R$0.00"


def test_main_registration():
    context = fake_context()
    a = contasFake({}, {})

    auth_service = fake_authService()

    transferCase = TransferFundsUseCase(a, context)
    openCase = OpenAccountUseCase(a, context, Password)
    get_balance_case = GetBalanceUseCase(a, context)
    get_accounts_case = GetAccountsUseCase(a, context)

    logged_cases = LoggedUseCases(
        transferCase,
        get_accounts_case,
        get_balance_case
    )
    unlogged_cases = UnloggedUseCases(openCase)

    i = inputfake(["3", "abc123", "pedro", "2"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[0] == "Your account has been successfully created!"


def test_trying_register_an_existed_account():
    context = fake_context()
    joao_login = "joao"
    joao_pw = Password("ab123")
    joao_acc = Account(1, [])
    a = contasFake({1: [joao_acc]}, {})

    auth_service = fake_authService()
    auth_service.accounts[joao_login] = (joao_pw, 1)

    transferCase = TransferFundsUseCase(a, context)
    openCase = OpenAccountUseCase(a, context, Password)
    get_balance_case = GetBalanceUseCase(a, context)
    get_accounts_case = GetAccountsUseCase(a, context)

    logged_cases = LoggedUseCases(
        transferCase,
        get_accounts_case,
        get_balance_case
    )
    unlogged_cases = UnloggedUseCases(openCase)

    i = inputfake(["3", "abc123", "joao", "2"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[0] == "Account already exists. Try another username."
