import re

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

num_pattern = r"[+-]?[1-9]+|[+-]?\d+(?:\.\d+)+"


def converter_validation(params: list) -> None:
    VALUE = params[1]
    UNIT1, UNIT2 = params[3].lower(), params[5].lower()

    # Ошибка 1: неизвестная еденица (например, byte)
    if UNIT1 not in units or UNIT2 not in units:
        raise UnknownUnit("неизвестная единица")

    # Ошибка 2: несовместимые еденицы (например, g и c)
    if units[UNIT1] != units[UNIT2]:
        raise IncompatibleUnits("несовместимые единицы")

    # Ошибка 3: неверное числовое значение (например, 1..2)
    if not re.fullmatch(num_pattern, VALUE):
        raise InvalidNumericalValue("неверное числовое значение")

    if (units[UNIT1] in ["length", "mass"] or UNIT1 == "k") and "-" in VALUE:
        raise InvalidNumericalValue("неверное числовое значение")
