import argparse

from .calculator import calc_validation, calculation, tokenization


def main():
    parser = argparse.ArgumentParser(prog="python -m toolkit")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Доступные команды"
    )

    # Настройка команды: calc
    parser_calc = subparsers.add_parser("calc", help="Калькулятор")
    parser_calc.add_argument("expression", type=str, help="Выражение для вычисления")

    # Настройка команды: convert
    parser_convert = subparsers.add_parser("convert", help="Конвертер")
    parser_convert.add_argument("value", type=float, help="Значение")
    parser_convert.add_argument(
        "--from", dest="from_unit", type=str, required=True, help="Исходная единица"
    )
    parser_convert.add_argument(
        "--to", dest="to_unit", type=str, required=True, help="Итоговая единица"
    )

    args = parser.parse_args()

    if args.command == "calc":
        calc_validation(args.expression)
        print(calculation(tokenization(args.expression)))
    elif args.command == "convert":
        print("Вызов convert")


if __name__ == "__main__":
    main()
