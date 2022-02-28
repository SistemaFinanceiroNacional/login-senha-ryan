import io
import cadastro_e_login


class inputfake():
    def __init__(self):
        self.inputlist = ["abc123","pedro","1"]
        self.outputlist = []

    def input(self, prompt):
        return self.inputlist.pop()

    def inputoccult(self, prompt):
        return self.inputlist.pop()

    def print(self, prompt):
        self.outputlist.append(prompt)

class inputfake2():
    def __init__(self):
        self.inputlist = ["abc123","pedro","2"]
        self.outputlist = []

    def input(self, prompt):
        return self.inputlist.pop()

    def inputoccult(self, prompt):
        return self.inputlist.pop()

    def print(self, prompt):
        self.outputlist.append(prompt)

class contasfake():
    def authentication(self,login,password):
        return login == "pedro" and password == "abc123"

class add_accountfake():
    def add_account(self,new_login,new_password):
        return new_login == "pedro" and new_password == "abc123"

def test_main():
    c = contasfake()
    i = inputfake()
    cadastro_e_login.main(c,i)
    assert i.outputlist[0] == "Você está logado!"

def test_main_choose_2_already_exist():
    i = inputfake2()
    c = add_accountfake()
    cadastro_e_login.main(c,i)
    assert i.outputlist[0] == "Conta criada com sucesso!"

def test_add_account():
    archive = io.StringIO("")
    new_login = "new_login"
    new_password = "new_password"
    x = cadastro_e_login.contas(archive)
    y = x.add_account(new_login,new_password)
    assert y

def test_add_existing_account():
    archive = io.StringIO("new_login:8f9afb58880507ec875fd077ed76abd4eeeff81e615648d8b8b00376d076b6e5eac0f98420341f61b07cb13f7540ae52c906014fd4412dcf56aeae8cfea2c005\n")
    new_login = "new_login"
    new_password = "new_password"
    x = cadastro_e_login.contas(archive)
    y = x.add_account(new_login, new_password)
    assert not y

def test_find_login():
    archive = io.StringIO("ask:ask\na:a\nb:b\nc:c\n")
    login = "a"
    x = cadastro_e_login.contas(archive).find_login(login)
    assert x

def test_hashpassword():
    x = cadastro_e_login.contas()
    password = "1"
    y = x.hashpassword(password)
    assert y == "4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a"

def test_authentication():
    archive = io.StringIO("initial:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b\n")
    l = "initial"
    s = "text"
    x = cadastro_e_login.contas(archive).authentication(l,s)
    assert x == True

def test_verify_correct_content():
    archive = io.StringIO("")
    y = inputfake2()
    x = cadastro_e_login.contas(archive)
    cadastro_e_login.main(x,y)
    assert archive.getvalue() == "pedro:c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc\n"

def test_verify_correct_content_using_different_password():
    archive = io.StringIO("pedro:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b\n")
    y = inputfake2()
    x = cadastro_e_login.contas(archive)
    cadastro_e_login.main(x,y)
    assert y.outputlist[0] == "Conta já existe. Tente outro usuário e senha."

def test_verify_content_from_last_test():
    archive = io.StringIO("pedro:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b\n")
    y = inputfake2()
    x = cadastro_e_login.contas(archive)
    cadastro_e_login.main(x, y)
    assert archive.getvalue() == "pedro:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b\n"