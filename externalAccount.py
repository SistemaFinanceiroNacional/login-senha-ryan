class externalAccount:
    def __init__(self,login):
        self.login = login
        self.balanceIncrement = 0

    def incrementBalance(self,value):
        if value < 0:
            raise negativeIncrementException(value)
        else:
            self.balanceIncrement += value

    def getIncrementBalance(self):
        return self.balanceIncrement

class negativeIncrementException(Exception):
    def __init__(self,value):
        self.value = value
        super().__init__(f"{self.value} is negative.")