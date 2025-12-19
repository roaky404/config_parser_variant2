# Парсер учебного конфигурационного языка (Вариант 2)

Инструмент командной строки для преобразования текста из учебного конфигурационного языка в JSON.

## Описание

Этот инструмент парсит конфигурационные файлы на специальном учебном языке и преобразует их в формат JSON. Реализован с использованием библиотеки Lark для синтаксического разбора.

Что умеет парсер:
- Числа и строки (типа @"текст")
- Массивы через array(...)
- Словари в begin...end
- Комментарии # и #|...|#
- Константы через <-
- Вычисления в ${...}
- Вложенные структуры

## Требования

- Python 3.6+
- Библиотека Lark-Parser

## Установка зависимостей

pip install lark-parser

## Использование

# Чтение из файла
python main.py -o output.json < config.txt

# В PowerShell
Get-Content config.txt | python main.py -o output.json

# В Command Prompt
type config.txt | python main.py -o output.json

## Примеры

### Пример 1: Конфигурация веб-сервера

**Файл:** `example1_web_server_simple.txt`

Get-Content example1_web_server_simple.txt | python main.py -o web_config.json

**Содержимое примера:**
# Простая конфигурация веб-сервера
server_name <- @"MyWebServer";
default_port <- 8080;

begin
  name := server_name;
  port := default_port;
  workers := array(@"worker1", @"worker2", @"worker3");
  
  settings := begin
    timeout := 30;
    max_connections := 1000;
    ssl_enabled := true;
  end;
  
  logging_level := @"INFO";
end

### Пример 2: Настройки компьютерной игры

**Файл:** `example2_game_settings_simple.txt`

Get-Content example2_game_settings_simple.txt | python main.py -o game_config.json

**Содержимое примера:**
# Простые настройки игры
game_name <- @"SuperGame";

begin
  game := begin
    title := game_name;
    version := @"1.0";
    difficulty := @"normal";
  end;
  
  graphics := begin
    resolution := array(1920, 1080);
    fullscreen := true;
    shadows := true;
  end;
  
  controls := begin
    up_key := @"W";
    action_key := @"SPACE";
    pause_key := @"P";
  end;
  
  features := array(@"multiplayer", @"achievements", @"cloud_save");
end

## Запуск тестов

# Все тесты
python -m unittest discover tests -v

# Конкретный тестовый файл
python -m unittest tests/test_parser.py -v

## Структура проекта

config_parser_variant2/
- main.py                 # Основной скрипт командной строки
- parser.py               # Парсер с использованием библиотеки Lark  
- README.md               # Эта документация
- .gitignore              # Игнорируемые файлы
- example1_web_server_simple.txt    # Пример 1: веб-сервер
- example2_game_settings_simple.txt # Пример 2: игра
- tests/                  # Модульные тесты
  - test_parser.py        # Тесты парсера
- .venv/                  # Виртуальное окружение (не в репозитории)
## Как работает

1. Читаем текст конфигурации
2. Разбираем его с помощью библиотеки Lark  
3. Преобразуем в Python-объекты
4. Сохраняем в JSON файл
## Автор

Бесчеревных Никита ИКБО-30-24

## Ссылка на репозиторий

https://github.com/roaky404/config_parser_variant2