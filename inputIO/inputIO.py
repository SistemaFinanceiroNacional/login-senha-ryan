import getpass

class inputIO:
    def input(self,prompt):
        return input(prompt)

    def inputoccult(self,prompt):
        return getpass.getpass(prompt)

    def print(self,prompt):
        print(prompt)