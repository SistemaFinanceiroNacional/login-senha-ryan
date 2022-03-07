import io
import cadastro_e_login


class inputfake():
    def __init__(self,lista):
        self.inputlist = lista # da última opção para a primeira
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

    def authentication(self,login,password):
        return login in self.actualAccounts and self.actualAccounts[login] == password

    def add_account(self,new_login,new_password):
        return new_login in self.newAccounts and self.newAccounts[new_login] == new_password

def conta_do_pedro_existente():
    return contasfake(actualAccounts={"pedro":"abc123"})

def conta_esperando_pedro():
    return contasfake(newAccounts={"pedro":"abc123"})

def empty_archive():
    return io.StringIO("")

def archive_with_pedro_and_his_password():
    return io.StringIO("pedro:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b\n")

def test_main_with_repl():
    c = conta_do_pedro_existente()
    i = inputfake(["sair","saldo","abc123","pedro","1"])
    cadastro_e_login.main(c,i)
    assert i.outputlist[0] == "0"

def test_main_choose_2_already_exist():
    i = inputfake(["abc123","pedro","2"])
    c = conta_esperando_pedro()
    cadastro_e_login.main(c,i)
    assert i.outputlist[0] == "Conta criada com sucesso!"

def test_add_account():
    archive = empty_archive()
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
    archive = empty_archive()
    y = inputfake(["abc123","pedro","2"])
    x = cadastro_e_login.contas(archive)
    cadastro_e_login.main(x,y)
    assert archive.getvalue() == "pedro:c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc\n"

def test_verify_correct_content_using_different_password():
    archive = archive_with_pedro_and_his_password()
    y = inputfake(["abc123","pedro","2"])
    x = cadastro_e_login.contas(archive)
    cadastro_e_login.main(x,y)
    assert y.outputlist[0] == "Conta já existe. Tente outro usuário e senha."

def test_verify_content_from_last_test():
    archive = archive_with_pedro_and_his_password()
    y = inputfake(["abc123","pedro","1"])
    x = cadastro_e_login.contas(archive)
    cadastro_e_login.main(x, y)
    assert archive.getvalue() == "pedro:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b\n"

def test_authentication_on_second_account():
    archive = io.StringIO("ryan:35ca097a8dab8ede4d632f41c909a3516a259e3b954f55b081f76e627d8a85cb81e91504a8fafc25e3a9074657550f6649029dca4b8c4253a67254b57b04131c\npedro:c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc\n")
    c = cadastro_e_login.contas(archive).authentication("pedro","abc123")
    assert c

def test_authentication_on_second_account_with_real_archive():
    with open("testbug.txt","r") as archive:
        c = cadastro_e_login.contas(archive).authentication("pedro","abc123")
        assert c