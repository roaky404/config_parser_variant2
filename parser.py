"""
Парсер для учебного конфигурационного языка (Вариант 2)
"""
import json
from lark import Lark, Transformer, Token


# Грамматика языка в формате Lark
GRAMMAR = """
    start: (constant | dict_block | array_block)*
    
    constant: NAME "<-" value ";"
    
    dict_block: "begin" pair* "end"
    pair: NAME ":=" value ";"
    
    array_block: "array" "(" [value ("," value)*] ")"
    
    value: NUMBER          -> number
         | STRING          -> string
         | array_block
         | dict_block
         | const_expr
         | NAME            -> name
    
    const_expr: "${" operation "}"
    operation: "+" value value -> add
             | "-" value value -> sub
             | "*" value value -> mul
             | "/" value value -> div
             | "len" "(" value ")" -> len
    
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
        text = str(items[0])
        return text[2:-1]  # Убираем @" и "

    def name(self, items):
        name = str(items[0])
        if name in self.constants:
            return self.constants[name]
        return name

    def array_block(self, items):
        # Преобразуем Tree в список
        if isinstance(items, list):
            return items
        elif hasattr(items, 'data') and items.data == 'value':
            # Это вложенный array_block внутри value
            return items.children[0] if items.children else []
        return list(items)

    def dict_block(self, items):
        result = {}
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                key, value = item
                result[key] = value
        return result

    def pair(self, items):
        key = str(items[0])
        value = items[1]
        return (key, value)

    def constant(self, items):
        name = str(items[0])
        value = items[1]
        self.constants[name] = value
        return ("constant", name, value)

    def add(self, items):
        left = items[0] if isinstance(items[0], (int, float)) else 0
        right = items[1] if isinstance(items[1], (int, float)) else 0
        return left + right

    def sub(self, items):
        left = items[0] if isinstance(items[0], (int, float)) else 0
        right = items[1] if isinstance(items[1], (int, float)) else 0
        return left - right

    def mul(self, items):
        left = items[0] if isinstance(items[0], (int, float)) else 0
        right = items[1] if isinstance(items[1], (int, float)) else 0
        return left * right

    def div(self, items):
        left = items[0] if isinstance(items[0], (int, float)) else 1
        right = items[1] if isinstance(items[1], (int, float)) else 1
        if right == 0:
            return 0
        return left / right

    def len(self, items):
        value = items[0]
        if isinstance(value, (list, dict, str)):
            return len(value)
        return 0

    def const_expr(self, items):
        return items[0]

    def value(self, items):
        # value может содержать array_block напрямую
        if len(items) == 1:
            return items[0]
        return items

    def start(self, items):
        result = {}
        for item in items:
            if isinstance(item, dict):
                result.update(item)
            elif isinstance(item, tuple) and item[0] == "constant":
                continue
            elif isinstance(item, list):
                if result:
                    # Если уже есть словарь, а тут массив - возвращаем словарь
                    continue
                return item
        return result


def parse_config(input_text: str):
    """Parse configuration text and return Python object"""
    parser = Lark(GRAMMAR, parser='lalr', transformer=ConfigTransformer())
    return parser.parse(input_text)


# Тест
if __name__ == "__main__":
    test = """
    begin
        name := @"test";
        value := 42;
    end
    """

    try:
        result = parse_config(test)
        print("Parsed successfully:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")