import cadastro_e_login

class inputfake:
    def __init__(self):
        self.inputlist = ["abc123","pedro","1"]
        self.outputlist = []

    def input(self, prompt):
        return self.inputlist.pop()

    def inputoccult(self, prompt):
        return self.inputlist.pop()

    def print(self, prompt):
        self.outputlist.append(prompt)

class contasfake:
    def authentication(self,login,password):
        return login == "pedro" and password == "abc123"


def test_main():
    c = contasfake()
    i = inputfake()
    cadastro_e_login.main(c,i)
    assert i.outputlist[0] == "Você está logado!"