import getpass

class inputIO:
    def input(self, prompt: str):
        return input(prompt)

    def inputoccult(self, prompt: str):
        return getpass.getpass(prompt)

    def print(self, prompt: str):
        print(prompt)