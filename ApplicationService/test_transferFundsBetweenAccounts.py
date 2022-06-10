import psycopg2
<<<<<<< HEAD
=======

>>>>>>> The transfer on transferFundsBetweenAccounts now can receive a destinyLogin and transform it into an externalAccount. We also initiated our web implementation.
import accounts
import externalAccountsInteractions
import internalAccount
from ApplicationService import transferFundsBetweenAccounts


def test_transfer_correct():
<<<<<<< HEAD
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (login text, password text, balance int);")
=======
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
    cursor = conn.cursor()
>>>>>>> The transfer on transferFundsBetweenAccounts now can receive a destinyLogin and transform it into an externalAccount. We also initiated our web implementation.
    loginOrigin = "login"
    passwordOrigin = "password"
    x = accounts.accounts(cursor)
    x.add_account(loginOrigin, passwordOrigin)

    extC = externalAccountsInteractions.externalAccountsInteractions(cursor)
    externalAccountOrigin = extC.getByLogin(loginOrigin).value
    externalAccountOrigin.incrementBalance(100)
    extC.update(loginOrigin, 100)

    loginDestiny = "loginDestiny"
    passwordDestiny = "passwordDestiny"
    x.add_account(loginDestiny, passwordDestiny)

    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    transferFundsBetweenAccounts.transferFundsBetweenAccountsClass(x, extC).execute(loggedAccount, loginDestiny, 100)

    destinyAccount = x.authentication(loginDestiny, passwordDestiny).value

    assert destinyAccount.balance() == 100
    cursor.close()
    conn.rollback()
    conn.close()


def test_transfer_correct2():
<<<<<<< HEAD
    conn = psycopg2.connect("dbname=test user=ryanbanco password='abc123' host=localhost")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (login text, password text, balance integer);")
    conn.commit()
=======
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
    cursor = conn.cursor()
>>>>>>> The transfer on transferFundsBetweenAccounts now can receive a destinyLogin and transform it into an externalAccount. We also initiated our web implementation.
    loginOrigin = "login"
    passwordOrigin = "password"
    x = accounts.accounts(cursor)
    x.add_account(loginOrigin, passwordOrigin)

    extC = externalAccountsInteractions.externalAccountsInteractions(cursor)
    externalAccountOrigin = extC.getByLogin(loginOrigin).value
    externalAccountOrigin.incrementBalance(100)
    externalAccountOrigin.update(extC)

    loginDestiny = "loginDestiny"
    passwordDestiny = "passwordDestiny"
    x.add_account(loginDestiny, passwordDestiny)

    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    transferFundsBetweenAccounts.transferFundsBetweenAccountsClass(x, extC).execute(loggedAccount, loginDestiny, 100)

    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    assert loggedAccount.balance() == 0
    cursor.close()
    conn.rollback()
    conn.close()


def test_transfer_zero_amout():
<<<<<<< HEAD
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
=======
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
>>>>>>> The transfer on transferFundsBetweenAccounts now can receive a destinyLogin and transform it into an externalAccount. We also initiated our web implementation.
    cursor = conn.cursor()
    loginOrigin = "login"
    passwordOrigin = "password"
    x = accounts.accounts(cursor)
    x.add_account(loginOrigin, passwordOrigin)

    loginDestiny = "loginDestiny"
    passwordDestiny = "passwordDestiny"
    x.add_account(loginDestiny, passwordDestiny)
    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    extC = externalAccountsInteractions.externalAccountsInteractions(cursor)

    try:
        transferFundsBetweenAccounts.transferFundsBetweenAccountsClass(x, extC).execute(loggedAccount, loginDestiny, 0)
        assert False

    except internalAccount.invalidValueToTransfer as e:
        assert e.value == 0

    cursor.close()
    conn.rollback()
    conn.close()


def test_transfer_negative_amout():
<<<<<<< HEAD
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
=======
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
>>>>>>> The transfer on transferFundsBetweenAccounts now can receive a destinyLogin and transform it into an externalAccount. We also initiated our web implementation.
    cursor = conn.cursor()
    loginOrigin = "login"
    passwordOrigin = "password"
    x = accounts.accounts(cursor)
    x.add_account(loginOrigin, passwordOrigin)

    loginDestiny = "loginDestiny"
    passwordDestiny = "passwordDestiny"
    x.add_account(loginDestiny, passwordDestiny)
    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    extC = externalAccountsInteractions.externalAccountsInteractions(cursor)

    try:
        transferFundsBetweenAccounts.transferFundsBetweenAccountsClass(x, extC).execute(loggedAccount, loginDestiny, -50)
        assert False

    except internalAccount.invalidValueToTransfer as e:
        assert e.value == -50

    cursor.close()
    conn.rollback()
    conn.close()


def test_transfer_not_existing_login_destiny():
<<<<<<< HEAD
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (login text, password text, balance int)")
=======
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
    cursor = conn.cursor()
>>>>>>> The transfer on transferFundsBetweenAccounts now can receive a destinyLogin and transform it into an externalAccount. We also initiated our web implementation.
    loginOrigin = "login"
    passwordOrigin = "password"
    x = accounts.accounts(cursor)
    x.add_account(loginOrigin, passwordOrigin)

    loginDestiny = "loginDestiny"
    loggedAccount = x.authentication(loginOrigin, passwordOrigin).value

    extC = externalAccountsInteractions.externalAccountsInteractions(cursor)

    try:
        transferFundsBetweenAccounts.transferFundsBetweenAccountsClass(x, extC).execute(loggedAccount, loginDestiny, -20)
        assert False
    except transferFundsBetweenAccounts.accountDoesNotExists as e:
        assert e.destinyLogin == loginDestiny

    cursor.close()
    conn.rollback()
    conn.close()
<<<<<<< HEAD


if __name__ == "__main__":
    test_transfer_correct2()
=======
>>>>>>> The transfer on transferFundsBetweenAccounts now can receive a destinyLogin and transform it into an externalAccount. We also initiated our web implementation.
