# Строки в Python

> **Зачем автотестеру:** Строки повсюду в тестировании — URL-адреса, JSON-ответы в виде текста, сообщения об ошибках, имена файлов, логи. Умение быстро разбирать, форматировать и проверять строки — базовый навык.

---

## Концепция

Строка (`str`) в Python — неизменяемая последовательность символов Unicode. Все методы строк возвращают **новую** строку, не изменяя оригинал.

```python
s = "Hello"
s.upper()   # "HELLO" — новая строка
print(s)    # "Hello" — оригинал не изменился
```

---

## Создание строк

```python
single = 'single quotes'
double = "double quotes"
multi  = """многострочная
строка"""
raw    = r"C:\Users\name"          # r-строка: обратный слеш не экранирует
byte   = b"bytes string"           # байтовая строка
```

---

## f-strings — форматирование строк

Самый современный и читаемый способ форматирования (Python 3.6+):

```python
name = "Alice"
age = 30
url = "https://api.example.com"

# Базовое использование
message = f"User {name} is {age} years old"

# Выражения внутри
result = f"2 + 2 = {2 + 2}"

# Форматирование чисел
price = 1234.5678
formatted = f"Price: {price:.2f}"       # "Price: 1234.57"

# Выравнивание
header = f"{'Name':<10} {'Age':>5}"     # "Name            Age"

# Отладка (Python 3.8+)
x = 42
debug = f"{x = }"   # "x = 42"
```

---

## Ключевые методы строк

| Метод | Что делает | Пример |
|-------|------------|--------|
| `split(sep)` | Разбивает по разделителю → `list` | `"a,b,c".split(",")` → `["a","b","c"]` |
| `split()` | Разбивает по пробелам (убирает пустые) | `"  a  b  ".split()` → `["a","b"]` |
| `join(iterable)` | Соединяет элементы через разделитель | `",".join(["a","b"])` → `"a,b"` |
| `strip()` | Убирает пробелы с обоих концов | `"  hello  ".strip()` → `"hello"` |
| `lstrip()` | Убирает пробелы слева | `"  hi".lstrip()` → `"hi"` |
| `rstrip()` | Убирает пробелы справа | `"hi  ".rstrip()` → `"hi"` |
| `upper()` | В верхний регистр | `"hello".upper()` → `"HELLO"` |
| `lower()` | В нижний регистр | `"HELLO".lower()` → `"hello"` |
| `replace(old, new)` | Заменяет подстроку | `"a-b".replace("-", "_")` → `"a_b"` |
| `startswith(prefix)` | Начинается ли с префикса | `"GET /api".startswith("GET")` → `True` |
| `endswith(suffix)` | Заканчивается ли суффиксом | `"file.json".endswith(".json")` → `True` |
| `find(sub)` | Индекс первого вхождения или `-1` | `"hello".find("ll")` → `2` |
| `in` | Проверка вхождения подстроки | `"api" in "/api/users"` → `True` |
| `count(sub)` | Число вхождений | `"aababc".count("ab")` → `2` |
| `isdigit()` | Только цифры? | `"123".isdigit()` → `True` |
| `isalpha()` | Только буквы? | `"abc".isalpha()` → `True` |

---

## Срезы строк

```python
s = "Hello, World!"
#    0123456789...

s[0]        # "H"         — первый символ
s[-1]       # "!"         — последний символ
s[0:5]      # "Hello"     — с 0 по 4
s[7:]       # "World!"    — с 7 до конца
s[:5]       # "Hello"     — с начала по 4
s[::2]      # "Hlo ol!"   — каждый второй
s[::-1]     # "!dlroW ,olleH"  — разворот строки
```

---

## Частые операции парсинга

### Разбор URL

```python
url = "https://api.example.com/v1/users?page=2&limit=10"

# Получить путь
path = url.split("?")[0]               # "https://api.example.com/v1/users"

# Получить query-параметры
query = url.split("?")[1]              # "page=2&limit=10"
params = dict(p.split("=") for p in query.split("&"))
# {"page": "2", "limit": "10"}
```

### Разбор строки с данными

```python
raw = "  John Doe; 25; john@example.com  "

parts = [p.strip() for p in raw.strip().split(";")]
# ["John Doe", "25", "john@example.com"]

name, age, email = parts
age_int = int(age)   # 25
```

### Проверка формата

```python
def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]

def is_valid_status_code(code: str) -> bool:
    return code.isdigit() and 100 <= int(code) <= 599
```

---

## Как это выглядит в pytest

### Тесты парсинга строк

```python
import pytest


def parse_csv_row(row: str) -> list[str]:
    """Парсит строку CSV, убирает пробелы у каждого поля."""
    return [field.strip() for field in row.split(",")]


def test_parse_csv_row_basic():
    assert parse_csv_row("Alice, 30, admin") == ["Alice", "30", "admin"]


def test_parse_csv_row_no_spaces():
    assert parse_csv_row("Alice,30,admin") == ["Alice", "30", "admin"]


def test_parse_csv_row_empty_fields():
    result = parse_csv_row("Alice,,admin")
    assert result == ["Alice", "", "admin"]


def test_parse_csv_row_single_field():
    assert parse_csv_row("Alice") == ["Alice"]
```

### Тест проверки URL-эндпоинта

```python
import pytest


def extract_endpoint(url: str) -> str:
    """Извлекает путь из URL без query-параметров."""
    return url.split("?")[0].split("//")[-1].split("/", 1)[-1]


@pytest.mark.parametrize("url,expected", [
    ("https://api.example.com/v1/users?page=1", "v1/users"),
    ("https://api.example.com/v1/orders", "v1/orders"),
    ("https://api.example.com/", ""),
])
def test_extract_endpoint(url: str, expected: str):
    assert extract_endpoint(url) == expected
```

### Проверка сообщения об ошибке в API-ответе

```python
def test_error_message_contains_field_name(api_client):
    response = api_client.post("/users", json={"name": ""})
    error_text = response.json()["message"]
    assert "name" in error_text.lower()
    assert response.status_code == 422
```

---

## Edge-кейсы

| Ситуация | Что происходит | Решение |
|----------|----------------|---------|
| `"".split(",")` | Возвращает `[""]`, а не `[]` | Проверяй `if s.strip()` перед split |
| `"a".split(",")` | Возвращает `["a"]` — нет разделителя | Обрабатывай случай одного элемента |
| `int("  42  ")` | `ValueError` | Сначала `.strip()`, потом `int()` |
| `int("")` | `ValueError` | Оборачивай в `try/except` |
| Строка с `\n` | `"line1\nline2".split()` убирает `\n` | Используй `splitlines()` для строк с переносами |
| Кодировка | `b"bytes".decode()` может упасть | Используй `decode("utf-8", errors="replace")` |

---

## Вопрос на собесе

**Q: В чём разница между `split()` и `split(",")`?**

> `split()` без аргумента разбивает по любому пробельному символу (пробел, таб, `\n`) и **убирает пустые элементы**. `split(",")` разбивает строго по запятой и **сохраняет пустые элементы** между двумя запятыми.

**Q: Как развернуть строку?**

> `s[::-1]` — срез с шагом `-1`. Это самый питонический способ.

**Q: Как проверить, что строка содержит только цифры?**

> `s.isdigit()` — но осторожно: возвращает `False` для `"-1"` и `"1.5"`. Для чисел с минусом/точкой лучше использовать `try: int(s)` или `try: float(s)`.
