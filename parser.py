"""
Парсер для учебного конфигурационного языка (Вариант 2)
"""
import json
from lark import Lark, Transformer, v_args

# Грамматика языка в формате Lark
GRAMMAR = """
    start: (constant | value)*

    constant: NAME "<-" value ";"

    value: NUMBER          -> number_value
         | STRING          -> string_value
         | array
         | dictionary
         | NAME            -> name_value
         | const_expr

    const_expr: "${" operation "}"

    operation: "+" value value -> add_op
             | "-" value value -> sub_op
             | "*" value value -> mul_op
             | "/" value value -> div_op
             | "len" "(" value ")" -> len_op

    array: "array" "(" [value ("," value)*] ")"

    dictionary: "begin" (assignment ";")+ "end"
    assignment: NAME ":=" value

    STRING: /@\"[^\"]*\"/
    NUMBER: /[+-]?\\d+/
    NAME: /[a-z][a-z0-9_]*/

    %import common.WS
    %ignore WS
    %ignore /#\\|[^|]*\\|#/
    %ignore /#[^\\n]*/
"""


class ConfigTransformer(Transformer):
    """Преобразует дерево разбора в Python-объекты"""

    def __init__(self):
        super().__init__()
        self.constants = {}

    def number_value(self, items):
        return int(items[0])

    def string_value(self, items):
        # Убираем @" и "
        text = str(items[0])
        return text[2:-1]

    def name_value(self, items):
        name = str(items[0])
        if name in self.constants:
            return self.constants[name]
        raise ValueError(f"Неизвестная константа: {name}")

    def array(self, items):
        return list(items)

    def dictionary(self, items):
        return dict(items)

    def assignment(self, items):
        return (str(items[0]), items[1])

    def constant(self, items):
        name = str(items[0])
        value = items[1]
        self.constants[name] = value
        return None

    def add_op(self, items):
        return items[0] + items[1]

    def sub_op(self, items):
        return items[0] - items[1]

    def mul_op(self, items):
        return items[0] * items[1]

    def div_op(self, items):
        return items[0] / items[1]

    def len_op(self, items):
        return len(items[0])

    def const_expr(self, items):
        return items[0]

    def start(self, items):
        # Фильтруем None (константы) и собираем все значения
        result = [item for item in items if item is not None]
        if len(result) == 1:
            return result[0]
        return result


def parse_config(input_text: str):
    """
    Парсит текст на учебном конфигурационном языке.
    Возвращает Python-объект (словарь, список, число, строку).
    """
    parser = Lark(GRAMMAR, parser='lalr', transformer=ConfigTransformer())
    try:
        return parser.parse(input_text)
    except Exception as e:
        raise ValueError(f"Ошибка разбора: {e}")


if __name__ == "__main__":
    # Тестовый пример
    test_input = """
    max_size <- 100;
    array(1, 2, 3, ${+ max_size 5})
    """

    try:
        result = parse_config(test_input)
        print("Результат разбора:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")