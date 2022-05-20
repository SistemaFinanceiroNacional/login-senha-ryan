import cadastro_e_login
import maybe
import account
import contas
import password

class inputfake():
    def __init__(self,lista):
        self.inputlist = lista
        self.outputlist = []

    def input(self, prompt):
        return self.inputlist.pop()

    def inputoccult(self, prompt):
        return self.inputlist.pop()

    def print(self, prompt):
        self.outputlist.append(prompt)


class contasfake():
    def __init__(self,actualAccounts=dict(),newAccounts=dict()):
        self.actualAccounts = actualAccounts
        self.newAccounts = newAccounts

    def authentication(self,login,user_password):
        hashsenha = password.password(self.actualAccounts[login][0])
        if login in self.actualAccounts and str(hashsenha) == str(user_password):
            return maybe.just(account.account(login,user_password,self.actualAccounts[login][1]))
        else:
            return maybe.nothing()

    def add_account(self,new_login,new_password):
        hashsenha = password.password(self.newAccounts[new_login])
        return new_login in self.newAccounts and str(hashsenha) == str(new_password)


class fakeCursor():
    def __init__(self,listSelect, listInsert):
        self.listSelect = listSelect
        self.listInsert = listInsert

    def select(self, columns, fromTable, where):
        return self.listSelect.pop()

    def insert(self, values, into):
        return self.listInsert.pop()


def conta_do_pedro_existente():
    return contasfake(actualAccounts={"pedro":("abc123","400")})

def conta_esperando_pedro():
    return contasfake(newAccounts={"pedro":"abc123"})


def test_main_with_repl():
    c = conta_do_pedro_existente()
    i = inputfake(["sair","saldo","abc123","pedro","1"])
    cadastro_e_login.main(c,i)
    assert i.outputlist[0] == "400"

def test_main_choose_2_already_exist():
    i = inputfake(["abc123","pedro","2"])
    c = conta_esperando_pedro()
    cadastro_e_login.main(c,i)
    assert i.outputlist[0] == "Conta criada com sucesso!"


def test_verify_correct_content():
    archive1 = [[]]
    archive2 = [[{"login":"pedro","password":"c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc","saldo":0}],[]]
    y = inputfake(["abc123","pedro","2"])
    x = contas.contas(fakeCursor(archive1,archive2))
    cadastro_e_login.main(x,y)
    assert archive2.pop().pop() == {"login":"pedro","password":"c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc","saldo":0}

def test_verify_correct_content_using_different_password():
    archive1 = [[{}]]
    archive2 = [[{"login":"pedro","password":"eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b","saldo":0}]]
    y = inputfake(["abc123","pedro","2"])
    x = contas.contas(fakeCursor(archive1,archive2))
    cadastro_e_login.main(x,y)
    assert y.outputlist[0] == "Conta já existe. Tente outro usuário e senha."

def test_verify_content_from_last_test():
    archive1 = [[{"login":"pedro","password":"eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b","saldo":0}]]
    archive2 = [[{"login":"pedro","password":"eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b","saldo":0}]]
    y = inputfake(["abc123","pedro","1"])
    x = contas.contas(fakeCursor(archive1,archive2))
    cadastro_e_login.main(x, y)
    assert archive2.pop().pop() == {"login":"pedro","password":"eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b","saldo":0}

if __name__ == "__main__":
    test_verify_correct_content()

