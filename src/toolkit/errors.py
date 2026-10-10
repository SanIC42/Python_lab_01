""" "Общие"""
class BaseError(Exception):
    pass


class TooManyArgs(BaseError):
    pass


class NotEnoughArgs(BaseError):
    pass


class InvalidNumericalValue(BaseError):
    pass


"""Калькулятор"""


class InvalidCharacter(BaseError):
    pass


class MissedOperand(BaseError):
    pass


class TwoBinaryOperatorsInARow(BaseError):
    pass


class DevisionByZero(BaseError):
    pass


class MissedOperator(BaseError):
    pass


"""Конвертер"""


class UnknownUnit(BaseError):
    pass


class IncompatibleUnits(BaseError):
    pass
