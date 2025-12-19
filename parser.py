"""
Парсер для учебного конфигурационного языка (Вариант 2)
"""
import json
from lark import Lark, Transformer, Token

# Грамматика языка в формате Lark
GRAMMAR = """
    start: (constant | dict_value)*

    constant: NAME "<-" value ";"

    value: NUMBER          -> number
         | STRING          -> string
         | array
         | dict_value
         | NAME            -> name
         | const_expr

    const_expr: "${" operation "}"

    operation: "+" value value -> add
             | "-" value value -> sub
             | "*" value value -> mul
             | "/" value value -> div
             | "len" "(" value ")" -> len

    array: "array" "(" [value ("," value)*] ")"

    dict_value: "begin" (pair ";")+ "end"
    pair: NAME ":=" value

    STRING: /@\"[^\"]*\"/
    NUMBER: /[+-]?\\d+/
    NAME: /[a-z][a-z0-9_]*/

    %import common.WS
    %ignore WS
    %ignore /#\\|[^|]*\\|#/
    %ignore /#[^\\n]*/
"""


class ConfigTransformer(Transformer):
    def __init__(self):
        self.constants = {}
        super().__init__()

    def number(self, items):
        return int(items[0])

    def string(self, items):
        text = items[0][2:-1]  # Remove @" and "
        return text

    def name(self, items):
        name = items[0]
        if name in self.constants:
            return self.constants[name]
        raise ValueError(f"Constant '{name}' not defined")

    def array(self, items):
        return list(items)

    def dict_value(self, items):
        result = {}
        for key, value in items:
            result[key] = value
        return result

    def pair(self, items):
        key = items[0]
        value = items[1]
        return (key, value)

    def constant(self, items):
        name = items[0]
        value = items[1]
        self.constants[name] = value
        return None

    def add(self, items):
        return items[0] + items[1]

    def sub(self, items):
        return items[0] - items[1]

    def mul(self, items):
        return items[0] * items[1]

    def div(self, items):
        return items[0] / items[1]

    def len(self, items):
        return len(items[0])

    def const_expr(self, items):
        return items[0]

    def start(self, items):
        # Filter out None values (constants)
        items = [item for item in items if item is not None]
        if not items:
            return {}
        # If multiple dicts, merge them
        result = {}
        for item in items:
            if isinstance(item, dict):
                result.update(item)
        return result


def parse_config(input_text: str):
    """Parse configuration text and return Python object"""
    parser = Lark(GRAMMAR, parser='lalr', transformer=ConfigTransformer())
    return parser.parse(input_text)


# Тест
if __name__ == "__main__":
    test = """
    port <- 8080;
    host <- @"localhost";

    begin
        server := host;
        port := port;
        workers := array(1, 2, 3);
    end
    """

    try:
        result = parse_config(test)
        print("Parsed successfully:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")