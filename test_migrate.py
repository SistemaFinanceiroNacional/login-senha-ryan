import migrate

class inputfake():
    def __init__(self,lista):
        self.inputlist = lista
        self.outputlist = []

    def input(self, prompt):
        return self.inputlist.pop()

    def inputoccult(self, prompt):
        return self.inputlist.pop()

    def print(self, prompt):
        self.outputlist.append(prompt)


def test_migrate_up():
    args = ["migrate.py", "up"]
    i = inputfake([])
    migrate.main(args, i)
    assert i.outputlist[0] == "up"

def test_migrate_down():
    args = ["migrate.py", "down"]
    i = inputfake([])
    migrate.main(args, i)
    assert i.outputlist[0] == "down"

def test_migrate_empty_folder():
    args = ["migrate.py", "--folder"]
    i = inputfake([])
    migrate.main(args, i)
    assert i.outputlist[0] == "Empty Folder"

def test_migrate_one_valid_argument():
    args = ["migrate.py", "--folder", "/testFolder"]
    i = inputfake([])
    migrate.main(args, i)
    assert i.outputlist[0] == "folder : /testFolder"

def test_migrate_two_valid_argument():
    args = ["migrate.py", "--folder", "/testFolder", "up"]
    i = inputfake([])
    migrate.main(args, i)
    assert i.outputlist[0] == "folder : /testFolder" and i.outputlist[1] == "up"
