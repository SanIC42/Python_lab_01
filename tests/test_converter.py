import pytest

from toolkit.converter import convert, convert_validation
from toolkit.errors import IncompatibleUnits, InvalidNumericalValue, UnknownUnit


def result(value: float, from_unit: str, to_unit: str) -> float:
    # Подсчёт конечного значения
    convert_validation(value, from_unit, to_unit)
    return convert(value, from_unit, to_unit)


"""Обязательные тесты"""


# (compulsory(англ.) - обязательный)
def test_compulsory_1():
    assert result(1000, "mm", "m") == 1


def test_compulsory_2():
    assert result(1.5, "kg", "g") == 1500


def test_compulsory_3():
    assert result(0, "c", "f") == 32


def test_compulsory_4():
    assert result(-273.15, "c", "k") == 0


def test_compulsory_5():
    assert result(-273.15, "c", "k") == 0


def test_compulsory_6_k():
    # Отрицательное значение температуры в к
    with pytest.raises(InvalidNumericalValue):
        convert_validation(-15, "k", "k")


def test_compulsory_6_c():
    # Температура в ц ниже абсолютного нуля
    with pytest.raises(InvalidNumericalValue):
        convert_validation(-273.2, "c", "c")


def test_compulsory_6_f():
    # Температура в ф ниже абсолютного нуля
    with pytest.raises(InvalidNumericalValue):
        convert_validation(-459.7, "f", "f")


def test_compulsory_7():
    # Несовместимые единицы измерения
    with pytest.raises(IncompatibleUnits):
        convert_validation(15, "kg", "m")


def test_compulsory_8():
    assert result(15_000_000, "mM", "KM") == 15


# Негативные тесты
def test_unknown_unit():
    # Неизвестная единица измерения
    with pytest.raises(UnknownUnit):
        convert_validation(8, "bit", "byte")



def test_kg_negative_value():
    # Отрицательное значение массы
    with pytest.raises(InvalidNumericalValue):
        convert_validation(-15, "kg", "kg")


def test_m_negative_value():
    # Отрицательное значение длины
    with pytest.raises(InvalidNumericalValue):
        convert_validation(-15, "m", "m")
