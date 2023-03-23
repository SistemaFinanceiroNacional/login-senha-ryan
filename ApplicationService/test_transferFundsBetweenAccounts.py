import psycopg2
import internalaccountsrepository
import externalaccountsinteractions
import internalAccount
from ApplicationService import transferFundsBetweenAccountsUseCase

class fakeCPool:
    def __init__(self):
        self.cursor = fakeCursor()

    def get_cursor(self):
        return self.cursor

class fakeCursor:
    pass

def test_transfer_correct():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (login text, password text, balance int);")
    loginOrigin = "login"
    passwordOrigin = "password"
    x = internalaccountsrepository.internalAccountsRepository(cursor)
    x.add_account(loginOrigin, passwordOrigin)

    extC = externalaccountsinteractions.externalAccountsInteractions(cursor)
    externalAccountOrigin = extC.get_by_login(loginOrigin).value
    externalAccountOrigin.incrementBalance(100)
    extC.update(loginOrigin, 100)

    loginDestiny = "loginDestiny"
    passwordDestiny = "passwordDestiny"
    x.add_account(loginDestiny, passwordDestiny)

    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    transferFundsBetweenAccountsUseCase.transferFundsBetweenAccountsUseCase(x, extC).execute(loggedAccount, loginDestiny, 100)

    destinyAccount = x.authentication(loginDestiny, passwordDestiny).value

    assert destinyAccount.balance() == 100
    cursor.close()
    conn.rollback()
    conn.close()


def test_transfer_correct2():
    conn = psycopg2.connect("dbname=test user=ryanbanco password='abc123' host=localhost")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (login text, password text, balance integer);")
    conn.commit()
    loginOrigin = "login"
    passwordOrigin = "password"
    x = internalaccountsrepository.internalAccountsRepository(cursor)
    x.add_account(loginOrigin, passwordOrigin)

    extC = externalaccountsinteractions.externalAccountsInteractions(cursor)
    externalAccountOrigin = extC.get_by_login(loginOrigin).value
    externalAccountOrigin.incrementBalance(100)
    externalAccountOrigin.update(extC)

    loginDestiny = "loginDestiny"
    passwordDestiny = "passwordDestiny"
    x.add_account(loginDestiny, passwordDestiny)

    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    transferFundsBetweenAccountsUseCase.transferFundsBetweenAccountsUseCase(x, extC).execute(loggedAccount, loginDestiny, 100)

    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    assert loggedAccount.balance() == 0
    cursor.close()
    conn.rollback()
    conn.close()


def test_transfer_zero_amout():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    loginOrigin = "login"
    passwordOrigin = "password"
    x = internalaccountsrepository.internalAccountsRepository()
    x.add_account(loginOrigin, passwordOrigin)

    loginDestiny = "loginDestiny"
    passwordDestiny = "passwordDestiny"
    x.add_account(loginDestiny, passwordDestiny)
    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    extC = externalaccountsinteractions.externalAccountsInteractions(cursor)

    try:
        transferFundsBetweenAccountsUseCase.transferFundsBetweenAccountsUseCase(x, extC).execute(loggedAccount, loginDestiny, 0)
        assert False

    except internalAccount.invalidValueToTransfer as e:
        assert e.value == 0

    cursor.close()
    conn.rollback()
    conn.close()


def test_transfer_negative_amount():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")

    cursor = conn.cursor()
    loginOrigin = "login"
    passwordOrigin = "password"
    x = internalaccountsrepository.internalAccountsRepository()
    x.add_account(loginOrigin, passwordOrigin)

    loginDestiny = "loginDestiny"
    passwordDestiny = "passwordDestiny"
    x.add_account(loginDestiny, passwordDestiny)
    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    extC = externalaccountsinteractions.externalAccountsInteractions(cursor)

    try:
        transferFundsBetweenAccountsUseCase.transferFundsBetweenAccountsUseCase(x, extC).execute(loggedAccount, loginDestiny, -50)
        assert False

    except internalAccount.invalidValueToTransfer as e:
        assert e.value == -50

    cursor.close()
    conn.rollback()
    conn.close()


def test_transfer_not_existing_login_destiny():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (login text, password text, balance int)")
    loginOrigin = "login"
    passwordOrigin = "password"
    x = internalaccountsrepository.internalAccountsRepository()
    x.add_account(loginOrigin, passwordOrigin)

    loginDestiny = "loginDestiny"
    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    extC = externalaccountsinteractions.externalAccountsInteractions(cursor)

    try:
        transferFundsBetweenAccountsUseCase.transferFundsBetweenAccountsUseCase(x, extC).execute(loggedAccount, loginDestiny, -20)
        assert False
    except transferFundsBetweenAccountsUseCase.accountDoesNotExists as e:
        assert e.destinyLogin == loginDestiny

    cursor.close()
    conn.rollback()
    conn.close()


if __name__ == "__main__":
    test_transfer_correct2()
