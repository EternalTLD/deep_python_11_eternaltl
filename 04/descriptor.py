from datetime import date


class CardType:
    ALLOWED_TYPES = ("VISA", "MASTERCARD", "MIR")

    def __set_name__(self, owner, name):
        self.name = name
        self._name = f"_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self._name)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError("Card type must be str")
        if value.upper() not in self.ALLOWED_TYPES:
            raise ValueError(f"Allowed card types: {', '.join(self.ALLOWED_TYPES)}")
        return setattr(obj, self._name, value.upper())


class CardNumber:
    def __set_name__(self, owner, name):
        self.name = name
        self._name = f"_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self._name)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError("Card number must be str")
        if len(value) != 16 or not value.isdigit():
            raise ValueError("Card number must consist of exactly 16 digits")

        return setattr(obj, self._name, value)


class ExpirationDate:
    def __set_name__(self, owner, name):
        self.name = name
        self._name = f"_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self._name)

    def __set__(self, obj, value):
        if not isinstance(value, date):
            raise TypeError("Expiration date must be datetime.date object")
        return setattr(obj, self._name, value)


class BankCard:
    card_type = CardType()
    number = CardNumber()
    expiration_date = ExpirationDate()

    def __init__(self, card_type, number, expiration_date):
        self.card_type = card_type
        self.number = number
        self.expiration_date = expiration_date
