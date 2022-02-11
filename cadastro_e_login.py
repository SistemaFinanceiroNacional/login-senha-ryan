import getpass
import hashlib

def main(contas,userIO):
    choose = userIO.input("Deseja fazer login (1) ou cadastro (2)?")
    if choose == "1":
        login = userIO.input("Informe o usuário: ")
        password = userIO.inputoccult("Informe a senha: ")
        if contas.authentication(login,password):
            userIO.print("Você está logado!")
        else:
            userIO.print("Você não está logado!")

    elif choose == "2":
        pass

class contas():
    def __init__(self,file=open("contas.txt","r")):
        self.archive = file

    def hashpassword(self,password):
        hash_password = hashlib.sha512(password.encode("utf-8"))
        return hash_password.hexdigest()

    def authentication(self,login,password):
        password = self.hashpassword(password)
        with self.archive as archive:
            for line in archive.readlines():
                line = line[:-1]
                logindoc,passworddoc = line.split(":")
                if login == logindoc and password == passworddoc:
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
    main(contas(),inputIO())