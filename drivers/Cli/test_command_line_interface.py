from drivers.Cli import command_line_interface
from ApplicationService.TransferFundsUseCase import TransferFundsUseCase
from ApplicationService.newbankaccountusecase import NewBankAccountUseCase
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.getBalanceUseCase import GetBalanceUseCase
from ApplicationService.getAccountsUseCase import GetAccountsUseCase
from ApplicationService.registerclientusecase import RegisterClientUseCase
from ApplicationService.gettransactionsusecase import GetTransactionsUseCase
from Domain.account import Account
from fake_config.fakes import (
    inputfake,
    clientsFake,
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
    c = clientsFake({joao_login: joao_pw})

    auth_service = fake_authService({joao_login: (joao_pw, 1)})

    transfer_case = TransferFundsUseCase(a, context)
    get_accounts_case = GetAccountsUseCase(a, context)
    get_balance_case = GetBalanceUseCase(a, context)
    get_transactions_case = GetTransactionsUseCase(a, context)
    new_bank_account_use_case = NewBankAccountUseCase(a, context)

    logged_cases = LoggedUseCases(
        transfer_case,
        get_accounts_case,
        get_balance_case,
        get_transactions_case,
        new_bank_account_use_case
    )

    register_client_use_case = RegisterClientUseCase(c, context, Password)
    unlogged_cases = UnloggedUseCases(register_client_use_case)

    i = inputfake(["3", "2", "4", "1", "1", "1", "abc123", "joao", "1"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[2] == "R$0.00"


def test_main_registration():
    context = fake_context()
    a = contasFake({}, {})
    c = clientsFake({})

    auth_service = fake_authService({})

    transfer_case = TransferFundsUseCase(a, context)
    get_accounts_case = GetAccountsUseCase(a, context)
    get_balance_case = GetBalanceUseCase(a, context)
    get_transactions_case = GetTransactionsUseCase(a, context)
    new_bank_account_use_case = NewBankAccountUseCase(a, context)

    logged_cases = LoggedUseCases(
        transfer_case,
        get_accounts_case,
        get_balance_case,
        get_transactions_case,
        new_bank_account_use_case
    )

    register_client_use_case = RegisterClientUseCase(c, context, Password)
    unlogged_cases = UnloggedUseCases(register_client_use_case)

    i = inputfake(["3", "abc123", "pedro", "2"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[0] == "Your account has been successfully created!"


def test_trying_register_an_existed_account():
    context = fake_context()
    joao_login = "joao"
    joao_pw = Password("ab123")
    joao_acc = Account(1, [])
    a = contasFake({1: [joao_acc]}, {})
    c = clientsFake({joao_login: joao_pw})

    auth_service = fake_authService({joao_login: (joao_pw, 1)})

    transfer_case = TransferFundsUseCase(a, context)
    get_accounts_case = GetAccountsUseCase(a, context)
    get_balance_case = GetBalanceUseCase(a, context)
    get_transactions_case = GetTransactionsUseCase(a, context)
    new_bank_account_use_case = NewBankAccountUseCase(a, context)

    logged_cases = LoggedUseCases(
        transfer_case,
        get_accounts_case,
        get_balance_case,
        get_transactions_case,
        new_bank_account_use_case
    )

    register_client_use_case = RegisterClientUseCase(c, context, Password)
    unlogged_cases = UnloggedUseCases(register_client_use_case)

    i = inputfake(["3", "abc123", "joao", "2"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[0] == "Account already exists. Try another username."
