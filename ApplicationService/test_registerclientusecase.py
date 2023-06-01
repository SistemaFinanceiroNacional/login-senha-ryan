from fake_config.fakes import clientsFake, fake_context
from ApplicationService.registerclientusecase import RegisterClientUseCase
from password import Password


def test_account_with_no_password_input():
    clients_rep = clientsFake({})
    cntx = fake_context()
    use_case = RegisterClientUseCase(clients_rep, cntx, Password)

    assert not use_case.execute('ryan', '')


def test_account_with_no_login_input():
    clients_rep = clientsFake({})
    cntx = fake_context()
    use_case = RegisterClientUseCase(clients_rep, cntx, Password)

    assert not use_case.execute('', 'abc123')
