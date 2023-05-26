from drivers.Cli import command_line_interface
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.OpenAccountUseCase import OpenAccountUseCase
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from Infrastructure.authServiceDB import AuthServiceDB
from Domain.account import Account
from fake_config.fakes import (
    inputfake,
    existing_pedros_account,
    waiting_pedro_account,
    fake_context,
    contasFake,
    fake_connection,
    fake_identity
)
from password import Password


def test_main_with_repl():
    context = fake_context()
    conn = fake_connection()
    iden = fake_identity(1)
    joao_login = "joao"
    joao_pw = Password("ab123")
    a = contasFake({}, {})
    a.add_account(joao_login, joao_pw)

    auth_service = AuthServiceDB(context, conn, iden)
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

    i = inputfake(["3", "logout", "balance", "abc123", "pedro", "1"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)
    assert i.outputlist[0] == 400


def test_main_choose_2_already_exist():
    context = fake_context()
    c = waiting_pedro_account()

    loginCase = loginUseCase(c, context, Password)
    transferCase = TransferFundsUseCase(c, context)
    openCase = OpenAccountUseCase(c, context, Password)

    i = inputfake(["3", "abc123", "pedro", "2"])

    command_line_interface.main(i, loginCase, transferCase, openCase)
    assert i.outputlist[0] == "Your account has been successfully created!"


def test_verify_correct_content_using_different_password():
    context = fake_context()
    c = existing_pedros_account()

    loginCase = loginUseCase(c, context, Password)
    transferCase = TransferFundsUseCase(c, context)
    openCase = OpenAccountUseCase(c, context, Password)

    i = inputfake(["3", "abc123", "pedro", "2"])

    command_line_interface.main(i, loginCase, transferCase, openCase)

    assert i.outputlist[0] == "Account already exists. Try another username."
