from drivers.cli import command_line_interface
from usecases.transfer import TransferFundsUseCase
from usecases.new_bank_account import NewBankAccountUseCase
from usecases.logged_cases import LoggedUseCases
from usecases.unlogged_cases import UnloggedUseCases
from usecases.get_balance import GetBalanceUseCase
from usecases.get_accounts import GetAccountsUseCase
from usecases.register_client import RegisterClientUseCase
from usecases.get_transactions import GetTransactionsUseCase
from domain.account import Account
from fake_config.fakes import (
    InputFake,
    ClientsFake,
    FakeContext,
    ContasFake,
    FakeAuthService
)
from password import Password


def test_main_login_and_balance():
    context = FakeContext()
    joao_login = "joao"
    joao_pw = Password("ab123")
    joao_acc = Account(1, [])
    a = ContasFake({1: [joao_acc]}, {})
    c = ClientsFake({joao_login: joao_pw})

    auth_service = FakeAuthService({joao_login: (joao_pw, 1)})

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

    i = InputFake(["3", "2", "4", "1", "1", "1", "abc123", "joao", "1"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[2] == "R$0.00"


def test_main_registration():
    context = FakeContext()
    a = ContasFake({}, {})
    c = ClientsFake({})

    auth_service = FakeAuthService({})

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

    i = InputFake(["3", "abc123", "pedro", "2"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[0] == "Your account has been successfully created!"


def test_trying_register_an_existed_account():
    context = FakeContext()
    joao_login = "joao"
    joao_pw = Password("ab123")
    joao_acc = Account(1, [])
    a = ContasFake({1: [joao_acc]}, {})
    c = ClientsFake({joao_login: joao_pw})

    auth_service = FakeAuthService({joao_login: (joao_pw, 1)})

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

    i = InputFake(["3", "abc123", "joao", "2"])

    command_line_interface.main(i, auth_service, unlogged_cases, logged_cases)

    assert i.outputlist[0] == "Account already exists. Try another username."
