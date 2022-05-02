import maybe
import account
import condition

class contas():
    def __init__(self,archiveCursor):
        self.archive = archiveCursor

    def __enter__(self):
        return self

    def add_account(self,new_login,new_password):
        x = self.archive.select(columns=["*"], fromTable="contas", where=condition.equal(condition.literal(new_login),condition.columnname("login")))

        if not x:
            self.archive.insert(values={"login":new_login,"password":new_password}, into="contas")

        return not x

    def authentication(self,login,password):
        findLoginList = self.archive.select(columns=["*"], fromTable="contas", where=condition.andCondition(condition.equal(condition.literal(login),condition.columnname("login")),condition.equal(condition.literal(password), condition.columnname("password"))))
        if len(findLoginList) == 1:
            findLoginValue = findLoginList[0]
            if str(password) == findLoginValue["password"]:
                return maybe.just(account.account(findLoginValue["login"],findLoginValue["password"],findLoginValue["saldo"]))
        return maybe.nothing()