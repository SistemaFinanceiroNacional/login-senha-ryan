from fake_config.fakes import contasFake, fake_context
from ApplicationService.openAccountUseCase import openAccountUseCase
from password import password


def test_account_with_no_password_input():
    internal_rep = contasFake({}, {})
    cntx = fake_context()
    use_case = openAccountUseCase(internal_rep, cntx, password)

    assert not use_case.execute('ryan', '')


def test_account_with_no_login_input():
    internal_rep = contasFake({}, {})
    cntx = fake_context()
    use_case = openAccountUseCase(internal_rep, cntx, password)

    assert not use_case.execute('', 'ab123')
