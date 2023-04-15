from ApplicationService.external_account import externalAccount, negativeIncrementException
from ApplicationService.internal_account import internalAccount, insufficientFundsException
from password import password

def test_transfer1():
    x = internalAccount("ryan", password("abc123"), 20)
    y = externalAccount("pedro")
    x.transfer(y, 10)
    assert x.get_balance() == 10

def test_incrementBalance1():
    x = externalAccount("pedro")
    try:
        x.increment_balance(-20)
        assert False
    except negativeIncrementException:
        assert True

def test_transfer_poor_ryan():
    x = internalAccount("ryan", password("abc123"), 10)
    y = externalAccount("pedro")
    try:
        x.transfer(y, 20)
        assert False
    except insufficientFundsException:
        assert True

def test_incrementBalance2():
    x = internalAccount("ryan", password("abc123"), 10)
    y = externalAccount("pedro")
    x.transfer(y, 10)
    assert y.get_increment_balance() == 10