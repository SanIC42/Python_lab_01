import operator
import re

from errors import (
    DevisionByZero,
    InvalidCharacter,
    InvalidNumericalValue,
    MissedOperand,
    MissedOperator,
    TwoBinaryOperatorsInARow,
)

num_pattern = r"\d+(?:\.\d+)?"


"""Проверкка входных данных на наличие ошибки"""


def calc_validation(input_string: str) -> None:
    # 1. Схлопываем лишние пробелы
    input_string = " ".join(input_string.split())

    if re.fullmatch(num_pattern, input_string):
        return

    # Шаблон для правильной строки от начала (^) до конца ($)
    # valid_string_pattern = rf"^[+-]?\s?{num_pattern}(?:\s?[+\-*/]\s?[+-]?{num_pattern}|\s?[*/]\s?[+-]\s?{num_pattern})+$"

    # Ошибка 1: Недопустимый символ (буквы, спецсимволы)
    if re.search(r"[A-Za-z!@#$%^&()?><;:`~_=]+", input_string):
        raise InvalidCharacter("недопустимый символ")

    # Ошибка 2: Пропущенный операнд (например, "1 + 2 +")
    if input_string[-1] in "-+*/":
        raise MissedOperand("пропущенный операнд")

    # Ошибка 3: Два бинарных оператора подряд (например, "1 + * 2")
    if re.search(
        r"[*/]\s?[*/]|[+\-]\s?[*/]|[+\-*/]\s?[+\-]\s?[+\-]", input_string
    ):
        raise TwoBinaryOperatorsInARow("два бинарных оператора подряд")

    # Ошибка 4: Деление на ноль (с учетом пробелов)
    if re.search(rf"{num_pattern}\s?/\s?[+\-]?0(?![.\d])", input_string):
        raise DevisionByZero("деление на ноль")

    # Ошибка 5: Два числа подряд через пробел (например, "1 + 2 3")
    if re.search(rf"{num_pattern} {num_pattern}", input_string):
        raise MissedOperator("пропущенный оператор")

    if re.search(r"\d*(?:\s?\.+\s?\d*)+", input_string):
        # Ошибка 6: Любые кривые числа вроде "005", "1..2" или ".5" без нуля
        raise InvalidNumericalValue("неверное числовое значение")


"""Токенизация входных данных"""


def tokenization(valid_string: str) -> list:
    # Токенизированный список
    res = valid_string.split()
    int_pattern = r"[+\-]?\d+"
    float_pattern = r"[+\-]?\d+(?:\.\d+)+"

    for i in range(len(res)):
        if re.fullmatch(int_pattern, res[i]):
            res[i] = int(res[i])
        elif re.fullmatch(float_pattern, res[i]):
            res[i] = float(res[i])

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
            # Пока на вершине стека оператор с БОЛЬШИМ или РАВНЫМ приоритетом,
            # мы выталкиваем его из стека в ОПН
            while stack and priorities[stack[-1]] >= priorities[token]:
                opn.append(stack.pop())
            # Кладем текущий оператор в стек
            stack.append(token)
        else:
            # Если токен - число, то просто добавляем в ОПН
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
            # Выполняем операцию над числами
            result = operations[token](a, b)
            stack.append(result)
        else:
            stack.append(token)

    return stack[0]


calc_validation(input())
