import re

num_pattern = r"\d+(?:\.\d+)?"


def tokenization(valid_string: str) -> list:
    # Паттерн: [знак] + [возможные пробелы] + [цифры] ИЛИ [оператор]
    pattern = rf"([+\-])?\s*({num_pattern})|([+\-*/])"

    res = []
    for elem in re.finditer(pattern, valid_string):
        unar_sign, num, operator = elem.groups()

        # Если нашли число (возможно со знаком)
        if num:
            # Если перед этим числом уже есть токены, и последний токен — ТОЖЕ число,
            # значит, этот знак был бинарным оператором (например, в "5 - 3")
            if res and isinstance(res[-1], (int, float)):
                # Возвращаем знак как отдельный оператор,
                # Число идёт без знака
                res.append(unar_sign)
                token = num
            else:
                # Склеиваем унарный знак с числом
                if unar_sign:
                    token = f"{unar_sign}{num}"
                else:
                    token = num
            # Приводим к типу int или float
            res.append(float(token) if "." in token else int(token))

        # Если нашли обычный оператор
        elif operator:
            res.append(operator)

    return res


print(tokenization(input()))
