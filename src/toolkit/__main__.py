import argparse
import sys

from toolkit.calculator import calc_validation, calculation, tokenization
from toolkit.converter import convert, convert_validation
from toolkit.errors import (
    DevisionByZero,
    IncompatibleUnits,
    InvalidCharacter,
    InvalidNumericalValue,
    MissedOperand,
    MissedOperator,
    TwoBinaryOperatorsInARow,
    UnknownUnit,
)


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
        try:
            calc_validation(args.expression)
            print(calculation(tokenization(args.expression)))
            sys.exit(0)
        except InvalidCharacter as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        except MissedOperand as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        except TwoBinaryOperatorsInARow as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        except DevisionByZero as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        except MissedOperator as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        except InvalidNumericalValue as e:
            print(e, file=sys.stderr)
            sys.exit(2)
    elif args.command == "convert":
        try:
            convert_validation(args.value, args.from_unit, args.to_unit)
            print(convert(args.value, args.from_unit, args.to_unit))
            sys.exit(0)
        except UnknownUnit as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        except IncompatibleUnits as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        except InvalidNumericalValue as e:
            print(e, file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
