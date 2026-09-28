from domain.money import InvalidMoney, Money, MoneyValue


class InvalidAmount(InvalidMoney):
    pass


class Amount(Money):
    """A quantity of money moved by an operation (a deposit, a transfer):
    always positive. Invalid values cannot be represented."""

    __slots__ = ()

    def __init__(self, value: MoneyValue):
        try:
            super().__init__(value)
        except InvalidMoney:
            raise InvalidAmount(value)
        if self.to_decimal() <= 0:
            raise InvalidAmount(value)
