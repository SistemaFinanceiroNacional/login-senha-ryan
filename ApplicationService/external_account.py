class externalAccount:
    def __init__(self, login: str):
        self._login = login
        self._balanceIncrement = 0

    def increment_balance(self, value: float) -> None:
        if value < 0:
            raise negativeIncrementException(value)
        else:
            self._balanceIncrement += value

    def get_increment_balance(self) -> int:
        return self._balanceIncrement

    def get_login(self) -> str:
        return self._login

class negativeIncrementException(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(f"{self.value} is negative.")
