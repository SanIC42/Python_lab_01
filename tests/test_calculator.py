import pytest

from toolkit.calculator import calc_validation, calculation, tokenization
from toolkit.errors import (
    DevisionByZero,
    EmptyExpression,
    InvalidCharacter,
    InvalidNumericalValue,
    MissedOperand,
    MissedOperator,
    TwoBinaryOperatorsInARow,
)


def result(input_string: str) -> int | float:
    # Подсчёт конечного значения
    calc_validation(input_string)
    return calculation(tokenization(input_string))


"""Обязательные тесты"""


# (compulsory(англ.) - обязательный)
def test_compulsory_1():
    assert result("2+3*4") == 14


def test_compulsory_2():
    assert result("10 / 4") == 2.5


def test_compulsory_3():
    assert result("-2 * -3") == 6


def test_compulsory_4():
    assert result("1+-2") == -1


def test_compulsory_5():
    # Пустое выражение
    with pytest.raises(EmptyExpression):
        calc_validation("   ")

def test_compulsory_6():
    # Два бинарных оператора подряд
    with pytest.raises(TwoBinaryOperatorsInARow):
        calc_validation("2*/3")

def test_compulsory_7():
    # Недопустимый символ
    with pytest.raises(InvalidCharacter):
        calc_validation("2+a")


def test_compulsory_8():
    # Деление на 0 с учётом пробелов
    with pytest.raises(DevisionByZero):
        calc_validation("1/0")


"""Кастомные тесты"""


def test_missed_operand():
    # Пропущенный операнд
    with pytest.raises(MissedOperand):
        calc_validation("1+2+")


def test_missed_operator():
    # Пропущенный оператор
    with pytest.raises(MissedOperator):
        calc_validation("1+2 3")


def test_invalid_numerical_value_many_dots():
    # Число с несколькими плавающими точками
    with pytest.raises(InvalidNumericalValue):
        calc_validation("1..")


def test_invalid_numerical_value_one_dot():
    # Некорректная запись числа с 1 плавающей точкой
    with pytest.raises(InvalidNumericalValue):
        calc_validation(".1")
