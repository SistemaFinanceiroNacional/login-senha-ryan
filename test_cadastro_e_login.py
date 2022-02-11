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

class contasfake():
    def authentication(self,login,password):
        return login == "pedro" and password == "abc123"




def test_main():
    c = contasfake()
    i = inputfake()
    cadastro_e_login.main(c,i)
    assert i.outputlist[0] == "Você está logado!"

def test_hashpassword():
    x = cadastro_e_login.contas()
    password = "1"
    y = x.hashpassword(password)
    assert y == "4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a"

def test_authentication():
    file = io.StringIO("initial:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b\n")
    l = "initial"
    s = "text"
    x = cadastro_e_login.contas(file).authentication(l,s)
    assert x == True
