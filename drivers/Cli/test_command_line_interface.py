from drivers.Cli import command_line_interface
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.OpenAccountUseCase import OpenAccountUseCase
from Domain.client import Client
from fake_config.fakes import (
    inputfake,
    existing_pedros_account,
    waiting_pedro_account,
    fake_context,
    clientsFake,
    contasFake
)
from password import Password


def test_main_with_repl():
    context = fake_context()
    joao_login = "joao"
    joao_pw = Password("ab123")
    joao_acc = Client(joao_login, joao_pw, [])
    c = clientsFake({joao_login: joao_acc})
    a = contasFake({}, {})

    loginCase = loginUseCase(c, context, Password)
    transferCase = TransferFundsUseCase(a, context)
    openCase = OpenAccountUseCase(a, context, Password)

    i = inputfake(["3", "logout", "balance", "abc123", "pedro", "1"])

    command_line_interface.main(i, loginCase, transferCase, openCase)
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
