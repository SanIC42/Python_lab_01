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


class EmptyExpression(Exception):
    pass


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


"""конвертер"""


class UnknownUnit(Exception):
    pass


class IncompatibleUnits(Exception):
    pass
