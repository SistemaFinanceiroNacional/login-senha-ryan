from ApplicationService.loginUseCase import loginUseCase
from fake_config.fakes import contasFake, fake_context
from password import Password
from maybe import isNothing


def test_login_with_no_password():
    internal_rep = contasFake({}, {})
    cntx = fake_context()
    use_case = loginUseCase(internal_rep, cntx, Password)

    assert isNothing(use_case.execute('ryan', ''))


def test_no_login():
    internal_rep = contasFake({}, {})
    cntx = fake_context()
    use_case = loginUseCase(internal_rep, cntx, Password)

    assert isNothing(use_case.execute('', 'abc123'))
