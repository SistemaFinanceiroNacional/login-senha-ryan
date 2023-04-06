from getpass import getpass

class inputIO:
    def input(self, prompt: str) -> input:
        return input(prompt)

    def inputoccult(self, prompt: str) -> getpass:
        return getpass(prompt)

    def print(self, prompt: str) -> None:
        print(prompt)