import operator
import re

from .errors import (
    DevisionByZero,
    InvalidCharacter,
    InvalidNumericalValue,
    MissedOperand,
    MissedOperator,
    TwoBinaryOperatorsInARow,
)

zero_pattern = r"(?<![.\d])0+(?![.\d])"
num_pattern = r"\d+(?:\.\d+)?"


"""Проверкка входных данных на наличие ошибки"""


def calc_validation(input_string: str) -> None:
    input_string = " ".join(input_string.split())

    if re.fullmatch(num_pattern, input_string):
        return

    # Ошибка 1: Недопустимый символ (буквы, спецсимволы)
    if re.search(r"[A-Za-z!@#$%^&()?><;:`~_=]+", input_string):
        raise InvalidCharacter("недопустимый символ")

    # Ошибка 2: Пропущенный операнд (например, "1 + 2 +")
    if input_string[-1] in "-+*/":
        raise MissedOperand("пропущенный операнд")

    # Ошибка 3: Два бинарных оператора подряд (например, "1 + * 2")
    if re.search(r"[*/]\s?[*/]|[+\-]\s?[*/]|[+\-*/]\s?[+\-]\s?[+\-]", input_string):
        raise TwoBinaryOperatorsInARow("два бинарных оператора подряд")

    # Ошибка 4: Деление на ноль (с учетом пробелов)
    if re.search(rf"{num_pattern}\s?/\s?[+\-]?\s?{zero_pattern}", input_string):
        raise DevisionByZero("деление на ноль")

    # Ошибка 5: Два числа подряд через пробел (например, "1 + 2 3")
    if re.search(rf"{num_pattern} {num_pattern}", input_string):
        raise MissedOperator("пропущенный оператор")

    # Ошибка 6: Любые кривые числа (например, "1..2", ".", ".5")
    if re.search(r"\.{2,}|(?<!\d)\.(?!\d)|\d+\.(?!\d)|(?<!\d)\.\d+", input_string):
        raise InvalidNumericalValue("неверное числовое значение")


"""Токенизация входных данных"""


def tokenization(valid_string: str) -> list:
    pattern = rf"([+\-])?\s*({num_pattern})|([+\-*/])"

    res = []
    for elem in re.finditer(pattern, valid_string):
        unar_sign, num, operator = elem.groups()

        # Если нашли число (возможно со знаком)
        if num:
            if res and isinstance(res[-1], (int, float)):
                res.append(unar_sign)
                token = num
            else:
                if unar_sign:
                    token = f"{unar_sign}{num}"
                else:
                    token = num
            res.append(float(token) if "." in token else int(token))

        # Если нашли обычный оператор
        elif operator:
            res.append(operator)

    return res


"""Вычисление значения выражения"""


def calculation(tokenized_string: list) -> int | float:
    # Обратная польская нотация
    opn = []
    # Стек
    stack = []
    # Приоритеты операций
    priorities = {"+": 1, "-": 1, "*": 2, "/": 2}

    for token in tokenized_string:
        # Быстрая проверка: если токен - оператор
        if token in priorities:
            while stack and priorities[stack[-1]] >= priorities[token]:
                opn.append(stack.pop())
            stack.append(token)
        # Если токен - число, то просто добавляем в ОПН
        else:
            opn.append(token)

    # Выталкиваем все оставшиеся операторы из стека в конец ОПН
    while stack:
        opn.append(stack.pop())

    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    for token in opn:
        if token in operations:
            # Вторым из стека достается ПРАВЫЙ операнд.
            # Первым из стека достается ЛЕВЫЙ операнд.
            b = stack.pop()
            a = stack.pop()

            result = operations[token](a, b)
            stack.append(result)
        else:
            stack.append(token)

    return stack[0]
