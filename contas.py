import maybe
import account

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
        fstr = f"{new_login}:{new_password}:0\n"
        if not x:
            self.archive.seek(0,2)
            self.archive.write(fstr)
        return not x

    def authentication(self,login,password):
        findLoginValue = self.find_login(login)
        if findLoginValue:
            if str(password) == findLoginValue[1]:
                return maybe.just(account.account(findLoginValue[0],findLoginValue[1],findLoginValue[2]))
        return maybe.nothing()