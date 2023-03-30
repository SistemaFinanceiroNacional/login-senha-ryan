class externalAccount:
    def __init__(self, login: str):
        self.login = login
        self.balanceIncrement = 0

    def incrementBalance(self, value: float):
        if value < 0:
            raise negativeIncrementException(value)
        else:
            self.balanceIncrement += value

    def getIncrementBalance(self):
        return self.balanceIncrement

    def update(self, repository):
        repository.update(self.login, self.balanceIncrement)

    def login(self):
        return self.login

class negativeIncrementException(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(f"{self.value} is negative.")
