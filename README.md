# Лабораторная работа 1. Консольный набор утилит


## Краткое Описание

Python-пакет с CLI, содержащий калькулятор и конвертер величин.


## Структура

<pre>
lab_01/
  pyproject.toml
  README.md
  src/toolkit/
    __init__.py
    __main__.py
    calculator.py
    converter.py
    errors.py
  tests/
</pre>


## Первая настройка

Выполнить в консоли:
```powershell
pip install -e .
```


## Команды

Справка:
```powershell
python -m toolkit --help
```

Калькулятор:
```powershell
python -m toolkit calc "EXPRESSION"
```

Конвертер:
```powershell
python -m toolkit convert VALUE --from UNIT --to UNIT
```


## Калькулятор

- Работает с целыми и вещественными числами.
- Использует операции `+`, `-`, `*`, `/`.
- Поддерживает `+` и `-` перед числом.
- Игнорирует пробелы между числами.
- Соблюдает приоритет `*` и `/` над `+` и `-`.

Использование:
```powershell
python -m toolkit calc "EXPRESSION"
```


## Конвертер

Работает о следующими группами величин:

- длина: `mm`, `cm`, `m`, `km`;
- масса: `g`, `kg`;
- температура: `c`, `f`, `k`.

Использование:
```powershell
python -m toolkit convert VALUE --from UNIT --to UNIT
```