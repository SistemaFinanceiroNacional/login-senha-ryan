from drivers.Cli import command_line_interface
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.transferFundsBetweenAccountsUseCase import transferFundsBetweenAccountsUseCase
from ApplicationService.openAccountUseCase import openAccountUseCase
from fake_config.fakes import inputfake, contasExternasFake, existing_pedros_account, waiting_pedro_account, \
    fake_context


def test_main_with_repl():
    context = fake_context()
    c = existing_pedros_account()
    extC = contasExternasFake({})

    loginCase = loginUseCase(c, context)
    transferCase = transferFundsBetweenAccountsUseCase(c, extC, context)
    openCase = openAccountUseCase(c, context)

    i = inputfake(["logout", "balance", "abc123", "pedro", "1"])

    command_line_interface.main(i, loginCase, transferCase, openCase)
    assert i.outputlist[0] == "400"


def test_main_choose_2_already_exist():
    context = fake_context()
    c = waiting_pedro_account()
    extC = contasExternasFake({})

    loginCase = loginUseCase(c, context)
    transferCase = transferFundsBetweenAccountsUseCase(c, extC, context)
    openCase = openAccountUseCase(c, context)

    i = inputfake(["abc123", "pedro", "2"])

    command_line_interface.main(i, loginCase, transferCase, openCase)
    assert i.outputlist[0] == "Your account has been successfully created!"


def test_verify_correct_content_using_different_password():
    context = fake_context()
    c = existing_pedros_account()
    extC = contasExternasFake({})

    loginCase = loginUseCase(c, context)
    transferCase = transferFundsBetweenAccountsUseCase(c, extC, context)
    openCase = openAccountUseCase(c, context)

    i = inputfake(["abc123", "pedro", "2"])

    command_line_interface.main(i, loginCase, transferCase, openCase)

    assert i.outputlist[0] == "Account already exists. Try another username."
