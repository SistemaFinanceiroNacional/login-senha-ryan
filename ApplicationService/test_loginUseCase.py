from ApplicationService.loginUseCase import loginUseCase
from fake_config.fakes import contasFake, fake_context
from password import password
from maybe import isNothing


def test_login_with_no_password():
    internal_rep = contasFake({}, {})
    cntx = fake_context()
    use_case = loginUseCase(internal_rep, cntx, password)

    assert isNothing(use_case.execute('ryan', ''))
