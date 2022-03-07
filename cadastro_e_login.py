import getpass
import hashlib

def repl(userIO,acc):
    comando = ""
    while comando != "sair":
        comando = userIO.input("->")
        if comando == "saldo":
            userIO.print(acc.saldo())


def main(contas,userIO):
    choose = userIO.input("Deseja fazer login (1) ou cadastro (2)? ")
    if choose == "1":
        login = userIO.input("Informe o usuário: ")
        password = userIO.inputoccult("Informe a senha: ")
        possible_account = contas.authentication(login,password)
        possible_account.map(lambda acc: repl(userIO,acc)).orElse(lambda : userIO.print("Você não está logado!"))


    elif choose == "2":
        login = userIO.input("Informe o seu novo usuário: ")
        password = userIO.inputoccult("Informe a sua nova senha: ")
        if contas.add_account(login,password):
            userIO.print("Conta criada com sucesso!")
        else:
            userIO.print("Conta já existe. Tente outro usuário e senha.")
            pass


class contas():
    def __init__(self,file=open("contas.txt","r+")):
        self.archive = file

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.archive.close()

    def find_login(self,login):
        self.archive.seek(0)
        for line in self.archive:
            line = line[:-1]
            logindoc,passworddoc,saldo = line.split(":")
            if login == logindoc:
                return (logindoc,passworddoc,saldo)
        return ()

    def add_account(self,new_login,new_password):
        x = self.find_login(new_login)
        new_password = self.hashpassword(new_password)
        fstr = f"{new_login}:{new_password}\n"
        if not x:
            self.archive.seek(0,2)
            self.archive.write(fstr)
        return not x

    def hashpassword(self,password):
        hash_password = hashlib.sha512(password.encode("utf-8"))
        return hash_password.hexdigest()

    def authentication(self,login,password):
        password = self.hashpassword(password)
        findLoginValue = self.find_login(login)
        if findLoginValue:
            if password == findLoginValue[1]:
                return just(account(findLoginValue[0],findLoginValue[1],findLoginValue[2]))
        return nothing()


class account():
    def __init__(self,login,senha,saldo):
        self.m_login = login
        self.m_senha = senha
        self.m_saldo = saldo

    def saldo(self):
        return self.m_saldo

    def __str__(self):
        x = f"login = {self.m_login}\nsenha = {self.m_senha}\nsaldo = {self.m_saldo}\n"
        return x

class maybe():
    def map(self,function):
        raise NotImplementedError

    def orElse(self,default):
        raise NotImplementedError

class just(maybe):
    def __init__(self,value):
        self.value = value

    def map(self,function):
        return just(function(self.value))

    def orElse(self,default):
        return self.value


class nothing(maybe):

    def map(self,function):
        return self

    def orElse(self,default):
        return default()


class inputIO():
    def input(self,prompt):
        return input(prompt)

    def inputoccult(self,prompt):
        return getpass.getpass(prompt)

    def print(self,prompt):
        print(prompt)




if __name__ == "__main__":
    with contas() as c:
        main(c,inputIO())