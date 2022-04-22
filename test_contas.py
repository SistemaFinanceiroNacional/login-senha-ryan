import contas
import cursor
import filemock
import io
import password


class fakeCursor():
    def __init__(self,cursor, dicio):
        self.cursor = cursor
        self.dicio = dicio

    def select(self):
        pass

    def insert(self):
        pass

def test_add_account():
    archive = filemock.empty_archive()
    new_login = "new_login"
    new_password = "new_password"
    x = contas.contas(archive)
    y = x.add_account(new_login,new_password)
    assert y

def test_add_existing_account():
    archive = io.StringIO("new_login:8f9afb58880507ec875fd077ed76abd4eeeff81e615648d8b8b00376d076b6e5eac0f98420341f61b07cb13f7540ae52c906014fd4412dcf56aeae8cfea2c005:150\n")
    new_login = "new_login"
    new_password = "new_password"
    x = contas.contas(archive)
    y = x.add_account(new_login, new_password)
    assert not y

def test_hashpassword():
    x = password.password("1")
    y = str(x)
    assert y == "4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a"

def test_authentication_just_or_nothing():
    archive = io.StringIO("initial:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b:1239\n")
    l = "initial"
    s = "text"
    passwordObject = password.password(s)
    x = contas.contas(archive).authentication(l,passwordObject)
    assert x.map(lambda _: True).orElse(lambda :False) == True

def test_authentication_on_second_account():
    archive = io.StringIO("ryan:35ca097a8dab8ede4d632f41c909a3516a259e3b954f55b081f76e627d8a85cb81e91504a8fafc25e3a9074657550f6649029dca4b8c4253a67254b57b04131c:17\npedro:c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc:1400\n")
    c = contas.contas(cursor.linearCursor()).authentication("pedro","abc123")
    assert c

def test_authentication_on_second_account_with_real_archive():
    with open("testbug.txt","r") as archive:
        c = contas.contas(fakeCursor.linearCursor()).authentication("pedro","abc123")
        assert c