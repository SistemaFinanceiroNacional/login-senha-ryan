import accounts
import externalAccount
import externalAccountsInteractions
import psycopg2

import internalAccount


def test_update1():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    loginUpdate = "loginUpdateTest"
    passwordUpdate = "passwordUpdateTest"
    x = accounts.accounts(cursor)
    x.add_account(loginUpdate,passwordUpdate)

    externalAccounts1 = externalAccountsInteractions.externalAccountsInteractions(cursor)
    accountToUpdate = externalAccounts1.getByLogin(loginUpdate).value
    accountToUpdate.incrementBalance(100)

    externalAccounts1.update(loginUpdate,accountToUpdate.getIncrementBalance())

    loggedAccount = x.authentication(loginUpdate,passwordUpdate).value
    cursor.close()
    conn.rollback()
    conn.close()
    assert loggedAccount.balance() == 100
