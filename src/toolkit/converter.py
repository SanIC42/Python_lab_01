from toolkit.errors import IncompatibleUnits, InvalidNumericalValue, UnknownUnit

units = {
    "mm": "length",
    "cm": "length",
    "m": "length",
    "km": "length",
    "g": "mass",
    "kg": "mass",
    "c": "temperature",
    "f": "temperature",
    "k": "temperature",
}

# Базовые единицы:
# Масса - г
# Длина - кг
# Температура - к
conversion_coeff = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
    "g": 1,
    "kg": 1000,
}


def converter_validation(value: float, from_unit: str, to_unit: str) -> None:
    """Проверкка входных данных на наличие ошибки"""

    from_unit, to_unit = from_unit.lower(), to_unit.lower()

    # Ошибка 1: неизвестная еденица (например, "byte")
    if from_unit not in units or to_unit not in units:
        raise UnknownUnit("неизвестная единица")

    # Ошибка 2: несовместимые еденицы (например, "g" и "c")
    if units[from_unit] != units[to_unit]:
        raise IncompatibleUnits("несовместимые единицы")

    # Ошибка 3: неверное числовое значение (отрицательная длина или недопустимая температура)
    if (units[from_unit] in ("length", "mass") or from_unit == "k") and value < 0:
        raise InvalidNumericalValue("неверное числовое значение")

    if units[from_unit] == "c" and value < -273.15:
        raise InvalidNumericalValue("неверное числовое значение")

    if units[from_unit] == "f" and value < -459.67:
        raise InvalidNumericalValue("неверное числовое значение")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Конвертация величины в"""

    category = units[from_unit]

    # Перевод для длины и массы
    if category in ("length", "mass"):
        base_value = value * conversion_coeff[from_unit]
        return base_value / conversion_coeff[to_unit]

    # Перевод для температуры
    if category == "temperature":
        if from_unit == "k":
            kelvins = value
        elif from_unit == "c":
            kelvins = value + 273.15
        elif from_unit == "f":
            kelvins = (value - 32) * 5 / 9 + 273.15

        if to_unit == "k":
            return kelvins
        elif to_unit == "c":
            return kelvins - 273.15
        elif to_unit == "f":
            return (kelvins - 273.15) * 9 / 5 + 32
