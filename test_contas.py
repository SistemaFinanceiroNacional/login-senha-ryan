import contas
import cursor
import filemock
import io
import password

# example of listoflistofdict = [[{"login":"pedro","password":"abc123"}]]

class fakeCursor():
    def __init__(self,listSelect, listInsert):
        self.listSelect = listSelect
        self.listInsert = listInsert

    def select(self, columns, fromTable, where):
        return self.listSelect.pop()

    def insert(self, values, into):
        return self.listInsert.pop()

def test_add_account():
    archiveList = [[]]
    archiveList2 = [[]]
    new_login = "new_login"
    new_password = "new_password"
    x = contas.contas(fakeCursor(archiveList,archiveList2))
    y = x.add_account(new_login,new_password)
    assert y

def test_add_existing_account():
    archiveList = [[{"login":"new_login","password":"new_password","saldo":0}]]
    archiveList2 = [[{"login":"new_login","password":"new_password","saldo":0}]]
    new_login = "new_login"
    new_password = "new_password"
    x = contas.contas(fakeCursor(archiveList,archiveList2))
    y = x.add_account(new_login, new_password)
    assert not y

def test_hashpassword():
    x = password.password("1")
    y = str(x)
    assert y == "4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a"

def test_authentication_just_or_nothing():################
    archiveList = [[{"login":"initial","password":"text","saldo":0}]]
    l = "initial"
    s = "text"
    x = contas.contas(fakeCursor(archiveList,archiveList)).authentication(l,s)
    assert x.map(lambda _: True).orElse(lambda _:False) == True

def test_authentication_on_second_account():
    archiveList = [[{"login":"ryan","password":"ab123","saldo":0},{"login":"pedro","password":"abc123","saldo":17}]]
    c = contas.contas(fakeCursor(archiveList,archiveList)).authentication("pedro","abc123")
    assert c


def test_authentication_on_second_account_with_real_archive():
    c = contas.contas(fakeCursor([[{"login":"pedro","password":"abc123","saldo":0}]],[[{"login":"pedro","password":"abc123","saldo":0}]])).authentication("pedro","abc123")
    assert c

if __name__ == "__main__":
    test_add_account()