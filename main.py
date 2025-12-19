#!/usr/bin/env python3
"""
Основной модуль утилиты для преобразования учебного конфигурационного языка в JSON.
"""
import sys
import json
import argparse
from parser import parse_config


def main():
    parser = argparse.ArgumentParser(description='Конвертер учебного конфигурационного языка в JSON.')
    parser.add_argument('-o', '--output', required=True, help='Путь к выходному JSON файлу.')
    args = parser.parse_args()

    # Чтение всего входного потока
    input_data = sys.stdin.read()

    try:
        # Парсим входные данные
        parsed_data = parse_config(input_data)

        # Запись результата в JSON файл
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        print(f"Конфигурация успешно сохранена в {args.output}", file=sys.stderr)

    except ValueError as e:
        print(f"Ошибка разбора: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка записи в файл: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()