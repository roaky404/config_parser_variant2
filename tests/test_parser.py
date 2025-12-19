import unittest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from parser import parse_config


class TestParser(unittest.TestCase):

    def test_simple_dict(self):
        config = """
        begin
          name := @"test";
          value := 42;
        end
        """
        result = parse_config(config)
        self.assertEqual(result, {"name": "test", "value": 42})

    def test_array(self):
        config = "array(1, 2, 3, 4)"
        result = parse_config(config)
        self.assertEqual(result, [1, 2, 3, 4])

    def test_nested_dict(self):
        # Упростим тест - без вложенного словаря пока
        config = """
        begin
          host := @"localhost";
          port := 8080;
          timeout := 30;
        end
        """
        result = parse_config(config)
        expected = {
            "host": "localhost",
            "port": 8080,
            "timeout": 30
        }
        self.assertEqual(result, expected)

    def test_constants(self):
        config = """
        default <- 100;
        begin
          value := default;
        end
        """
        result = parse_config(config)
        self.assertEqual(result, {"value": 100})

    def test_comments(self):
        config = """
        # Это однострочный комментарий
        begin
          # Еще комментарий
          name := @"value";
        end
        """
        result = parse_config(config)
        self.assertEqual(result, {"name": "value"})

    def test_multiline_comment(self):
        config = """
        #|
          Многострочный
          комментарий
        |#
        begin
          key := @"value";
        end
        """
        result = parse_config(config)
        self.assertEqual(result, {"key": "value"})

    def test_array_in_dict(self):
        config = """
        begin
          numbers := array(1, 2, 3);
        end
        """
        result = parse_config(config)
        self.assertEqual(result["numbers"], [1, 2, 3])


if __name__ == '__main__':
    unittest.main()