from getpass import getpass


class inputIO:
    def input(self, prompt: str) -> str:
        return input(prompt)

    def inputoccult(self, prompt: str) -> str:
        return getpass(prompt)

    def print(self, prompt: str) -> None:
        print(prompt)
