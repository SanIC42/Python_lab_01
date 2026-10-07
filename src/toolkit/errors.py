""" "Общие"""


class TooManyArgs(Exception):
    pass


class NotEnoughArgs(Exception):
    pass


class InvalidCommand(Exception):
    pass


class InvalidNumericalValue(Exception):
    pass


"""Калькулятор"""


class InvalidCharacter(Exception):
    pass


class MissedOperand(Exception):
    pass


class TwoBinaryOperatorsInARow(Exception):
    pass


class DevisionByZero(Exception):
    pass


class MissedOperator(Exception):
    pass


"""Конвертер"""


class UnknownUnit(Exception):
    pass


class IncompatibleUnits(Exception):
    pass
