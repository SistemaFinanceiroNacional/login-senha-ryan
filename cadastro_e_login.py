import getpass
import hashlib

def repl(userIO):
    comando = ""
    while comando != "sair":
        comando = userIO.input("->")
        if comando == "saldo":
            userIO.print("0")


def main(contas,userIO):
    choose = userIO.input("Deseja fazer login (1) ou cadastro (2)?")
    if choose == "1":
        login = userIO.input("Informe o usuário: ")
        password = userIO.inputoccult("Informe a senha: ")
        if contas.authentication(login,password):
            repl(userIO)
        else:
            userIO.print("Você não está logado!")

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
        x = 0
        for line in self.archive.readlines():
            line = line[:-1]
            logindoc,_ = line.split(":")
            if login == logindoc:
                self.archive.seek(x,0)
                return True
            else:
                x += len(line)+1
        return False

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
        if self.find_login(login):
            x = self.archive.readline()[:-1]
            _,passworddoc = x.split(":")
            if password == passworddoc:
                return True
        return False

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