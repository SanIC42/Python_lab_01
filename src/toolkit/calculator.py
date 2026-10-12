import operator
import re

from toolkit.errors import (
    DevisionByZero,
    EmptyExpression,
    InvalidCharacter,
    InvalidNumericalValue,
    MissedOperand,
    MissedOperator,
    TwoBinaryOperatorsInARow,
)

# Паттерн одиночного нуля
zero_pattern = r"(?<![.\d])0+(?![.\d])"
# Паттерн числа
num_pattern = r"\d+(?:\.\d+)?"


def calc_validation(input_string: str) -> None:
    """Проверкка входных данных на наличие ошибки"""

    input_string = " ".join(input_string.split())

    if re.fullmatch(num_pattern, input_string):
        return

    if input_string == "":
        raise EmptyExpression("пустое выражение")

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


def tokenization(valid_string: str) -> list:
    # Паттерн токена (число либо оператор)
    pattern = rf"({num_pattern})|([+\-*/])"
    # Токенизированная строка
    res = []

    for elem in re.finditer(pattern, valid_string):
        num, operator = elem.groups()

        # Если число, то пытаемся
        # склеить его с унарным знаком, идущим до него,
        # или просто добавляем его в res
        if num:
            if res and res[-1] in "+-" and (len(res) == 1 or type(res[-2]) == str):
                res = res[:-1] + [float(f"{res[-1]}{num}")]
            else:
                res.append(float(num))
        # Если строка, то просто добваляем в res
        else:
            res.append(operator)

    return res


def calculation(tokenized_string: list) -> float:
    """Вычисление значения выражения"""

    # Обратная польская нотация
    opn = []
    # Стек
    stack = []
    # Приоритеты операций
    priorities = {"+": 1, "-": 1, "*": 2, "/": 2}

    # Формирование обратной польской нотации (ОПН)
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
    opn += stack[::-1]
    stack = []

    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    # Подсчёт выражения
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
