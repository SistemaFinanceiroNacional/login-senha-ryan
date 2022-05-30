import psycopg2
import accounts
import filemock
import io
import password

# example of listoflistofdict = [[{"login":"pedro","password":"abc123"}]]

def test_add_account():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
    cursor = conn.cursor()
    new_login = "new_login"
    new_password = "new_password"
    x = accounts.accounts(cursor)
    y = x.add_account(new_login,new_password)
    cursor.close()
    conn.rollback()
    conn.close()
    assert y

def test_add_existing_account():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
    cursor = conn.cursor()
    x = accounts.accounts(cursor)
    existing_login = "same_login"
    existing_password = "same_password"
    firstAdd = x.add_account(existing_login,existing_password)
    new_login = "same_login"
    new_password = "same_password"
    y = x.add_account(new_login, new_password)
    cursor.close()
    conn.rollback()
    conn.close()
    assert not y

def test_hashpassword():
    x = password.password("1")
    y = str(x)
    assert y == "4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a"

def test_authentication_just_or_nothing():################
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
    cursor = conn.cursor()
    x = accounts.accounts(cursor)
    l = "initial"
    s = password.password("text")
    x.add_account(l,s)
    y = x.authentication(l,s)
    cursor.close()
    conn.rollback()
    conn.close()
    assert y.map(lambda _: True).orElse(lambda : False) == True

def test_authentication_on_second_account():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123")
    cursor = conn.cursor()
    x = accounts.accounts(cursor)
    login1 = "ryan"
    senha1 = password.password("ab123")
    x.add_account(login1, senha1)
    login2 = "pedro"
    senha2 = password.password("abc123")
    x.add_account(login2,senha2)
    c = x.authentication(login2, senha2)
    cursor.close()
    conn.rollback()
    conn.close()
    assert c.map(lambda _: True).orElse(lambda : False) == True

if __name__ == "__main__":
    test_add_account()