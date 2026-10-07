from src.toolkit.errors import IncompatibleUnits, InvalidNumericalValue, UnknownUnit

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


def converter_validation(value: float, from_unit: str, to_unit: str) -> None:
    """Проверкка входных данных на наличие ошибки"""

    from_unit, to_unit = from_unit.lower(), to_unit.lower()

    # Ошибка 1: неизвестная еденица (например, "byte")
    if from_unit not in units or to_unit not in units:
        raise UnknownUnit("неизвестная единица")

    # Ошибка 2: несовместимые еденицы (например, "g" и "c")
    if units[from_unit] != units[to_unit]:
        raise IncompatibleUnits("несовместимые единицы")

    # Ошибка 3: неверное числовое значение (например, "-154")
    if (units[from_unit] in ["length", "mass"] or from_unit == "k") and value < 0:
        raise InvalidNumericalValue("неверное числовое значение")
