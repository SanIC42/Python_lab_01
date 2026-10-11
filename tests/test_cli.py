import sys

import pytest

from toolkit.__main__ import main


def run_main(args: list, capsys) -> tuple[int, str, str]:
    sys.argv[1:] = args

    # Сохраняем информацию о выводах и ошибках в переменную exc_info
    with pytest.raises(SystemExit) as exc_info:
        main()

    # Захватываем потоки вывода
    captured = capsys.readouterr()

    return exc_info.value.code, captured.out.strip(), captured.err.strip()


"""Калькулятор"""


# Позитивный тест
def test_calculator_success(capsys):
    exit_code, stdout, stderr = run_main(["calc", "+1+ -2*-1"], capsys)

    assert exit_code == 0
    assert stdout == "3.0"
    assert stderr == ""


# Негативный тест
def test_calculator_invalid_character(capsys):
    exit_code, stdout, stderr = run_main(["calc", "1+a"], capsys)

    assert exit_code == 2
    assert stdout == ""
    assert stderr == "недопустимый символ"


"""Конвертер"""


# Позитивный тест
def test_converter_success(capsys):
    exit_code, stdout, stderr = run_main(
        ["convert", "2", "--from", "kg", "--to", "g"], capsys
    )

    assert exit_code == 0
    assert stdout == "2000.0"
    assert stderr == ""


# Негативный тест
def test_converter_unknown_unit(capsys):
    exit_code, stdout, stderr = run_main(
        ["convert", "8", "--from", "bit", "--to", "byte"], capsys
    )

    assert exit_code == 2
    assert stdout == ""
    assert stderr == "неизвестная единица"
