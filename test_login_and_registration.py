import externalAccountsInteractions
import login_and_registration
import maybe
import internalAccount
import accounts
import password
import psycopg2

class inputfake:
    def __init__(self,lista):
        self.inputlist = lista
        self.outputlist = []

    def input(self, prompt):
        return self.inputlist.pop()

    def inputoccult(self, prompt):
        return self.inputlist.pop()

    def print(self, prompt):
        self.outputlist.append(prompt)


class contasfake:
    def __init__(self,actualAccounts=dict(),newAccounts=dict()):
        self.actualAccounts = actualAccounts
        self.newAccounts = newAccounts

    def authentication(self,login,user_password):
        hashsenha = password.password(self.actualAccounts[login][0])
        if login in self.actualAccounts and str(hashsenha) == str(user_password):
            return maybe.just(internalAccount.internalAccount(login, user_password, self.actualAccounts[login][1]))
        else:
            return maybe.nothing()

    def add_account(self,new_login,new_password):
        hashsenha = password.password(self.newAccounts[new_login])
        return new_login in self.newAccounts and str(hashsenha) == str(new_password)


def existing_pedros_account():
    return contasfake(actualAccounts={"pedro":("abc123","400")})

def waiting_pedro_account():
    return contasfake(newAccounts={"pedro":"abc123"})


def test_main_with_repl():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    c = existing_pedros_account()
    i = inputfake(["logout","balance","abc123","pedro","1"])
    z = externalAccountsInteractions.externalAccountsInteractions(cursor)
    login_and_registration.main(c,z,i)
    assert i.outputlist[0] == "400"

def test_main_choose_2_already_exist():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    i = inputfake(["abc123","pedro","2"])
    c = waiting_pedro_account()
    z = externalAccountsInteractions.externalAccountsInteractions(cursor)
    login_and_registration.main(c,z,i)
    assert i.outputlist[0] == "Your account has been successfully created!"

def test_verify_correct_content_using_different_password():
    conn = psycopg2.connect("dbname=test user=ryanbanco password=abc123 host=localhost")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (login text, password text, balance int)")
    x = accounts.accounts(cursor)
    new_login = "pedro"
    new_password = password.password("ab123")
    x.add_account(new_login,new_password)
    y = inputfake(["abc123","pedro","2"])
    z = externalAccountsInteractions.externalAccountsInteractions(cursor)
    login_and_registration.main(x,z,y)
    cursor.close()
    conn.rollback()
    conn.close()
    assert y.outputlist[0] == "Account already exists. Try another username and password."

if __name__ == "__main__":
    test_verify_correct_content_using_different_password()

