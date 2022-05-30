import accounts
import externalAccount
import internalAccount

def test_transfer1():
    x = internalAccount.internalAccount("ryan","abc123",20)
    y = externalAccount.externalAccount("pedro")
    x.transfer(y, 10)
    assert x.balance() == 10

def test_incrementBalance1():
    x = externalAccount.externalAccount("pedro")
    try:
        x.incrementBalance(-20)
        assert False
    except externalAccount.negativeIncrementException as err:
        assert True

def test_transfer_poor_ryan():
    x = internalAccount.internalAccount("ryan", "abc123", 10)
    y = externalAccount.externalAccount("pedro")
    try:
        x.transfer(y,20)
        assert False
    except internalAccount.insufficientFundsException as err:
        assert True

def test_incrementBalance2():
    x = internalAccount.internalAccount("ryan", "abc123", 10)
    y = externalAccount.externalAccount("pedro")
    x.transfer(y, 10)
    assert y.getIncrementBalance() == 10