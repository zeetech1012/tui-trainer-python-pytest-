# Функции в Python

> **Зачем автотестеру:** Функции — строительный блок любого теста. Каждый тест в pytest — это функция. Понимание аргументов, возвращаемых значений и type hints обязательно для написания читаемых и переиспользуемых хелперов и фикстур.

---

## Концепция

Функция — именованный блок кода, который можно вызвать многократно. В Python функции являются объектами первого класса: их можно передавать как аргументы, хранить в переменных и возвращать из других функций.

---

## Базовый синтаксис

```python
def function_name(param1: type, param2: type) -> return_type:
    """Docstring: что делает функция."""
    result = param1 + param2
    return result
```

### Минимальный пример

```python
def add(a: int, b: int) -> int:
    return a + b

result = add(3, 5)   # 8
```

---

## Виды аргументов

### 1. Позиционные аргументы

```python
def greet(name: str, greeting: str) -> str:
    return f"{greeting}, {name}!"

greet("Alice", "Hello")   # "Hello, Alice!"
```

### 2. Аргументы по умолчанию

```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

greet("Alice")             # "Hello, Alice!"
greet("Bob", "Hi")         # "Hi, Bob!"
```

> **Ловушка:** никогда не используй изменяемый объект как значение по умолчанию!

```python
# НЕПРАВИЛЬНО — список разделяется между всеми вызовами
def append_item(item: str, items: list = []) -> list:
    items.append(item)
    return items

# ПРАВИЛЬНО
def append_item(item: str, items: list | None = None) -> list:
    if items is None:
        items = []
    items.append(item)
    return items
```

### 3. `*args` — произвольное число позиционных аргументов

```python
def sum_all(*args: int) -> int:
    return sum(args)

sum_all(1, 2, 3)       # 6
sum_all(10, 20)        # 30
```

### 4. `**kwargs` — произвольное число именованных аргументов

```python
def build_request(**kwargs: str) -> dict:
    return dict(kwargs)

build_request(method="GET", url="/api/users", token="abc123")
# {"method": "GET", "url": "/api/users", "token": "abc123"}
```

### 5. Keyword-only аргументы (после `*`)

```python
def send_request(url: str, *, method: str = "GET", timeout: int = 5) -> dict:
    # method и timeout обязаны передаваться по имени
    return {"url": url, "method": method, "timeout": timeout}

send_request("/api/users", method="POST", timeout=10)
```

---

## Type hints — аннотации типов

```python
from typing import Optional, Union, List

def find_user(user_id: int) -> Optional[dict]:
    """Возвращает dict или None если не найден."""
    ...

def parse_ids(data: str | list) -> list[int]:
    """str или list -> list[int]"""
    if isinstance(data, str):
        return [int(x) for x in data.split(",")]
    return [int(x) for x in data]
```

---

## Lambda — анонимные функции

```python
# Обычная функция
def double(x: int) -> int:
    return x * 2

# То же самое через lambda
double = lambda x: x * 2

# Практическое применение — сортировка
users = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]
sorted_users = sorted(users, key=lambda u: u["age"])
```

---

## Как это выглядит в pytest

### Хелпер-функция для генерации тестовых данных

```python
def make_order(
    product_id: int = 1,
    quantity: int = 1,
    status: str = "pending",
) -> dict:
    """Фабрика тестовых данных для заказа."""
    return {
        "product_id": product_id,
        "quantity": quantity,
        "status": status,
        "total": product_id * quantity * 100,
    }


def test_order_total_calculation():
    order = make_order(product_id=5, quantity=3)
    assert order["total"] == 1500


def test_order_default_status():
    order = make_order()
    assert order["status"] == "pending"
```

### Функция с `*args` в тесте

```python
def validate_keys(response: dict, *required_keys: str) -> bool:
    return all(key in response for key in required_keys)


def test_response_has_required_fields():
    response = {"id": 1, "name": "Alice", "email": "alice@example.com"}
    assert validate_keys(response, "id", "name", "email")


def test_response_missing_field():
    response = {"id": 1, "name": "Alice"}
    assert not validate_keys(response, "id", "name", "email")
```

### Функция с `**kwargs` — гибкий билдер запроса

```python
import pytest


def build_headers(**kwargs: str) -> dict:
    base = {"Content-Type": "application/json"}
    base.update(kwargs)
    return base


@pytest.mark.parametrize("extra,expected_key", [
    ({"Authorization": "Bearer token123"}, "Authorization"),
    ({"X-Request-ID": "abc"}, "X-Request-ID"),
])
def test_build_headers_adds_extra(extra: dict, expected_key: str):
    headers = build_headers(**extra)
    assert expected_key in headers
    assert "Content-Type" in headers
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Мутабельный дефолт | `def f(lst=[])` — список один на все вызовы | Используй `None` как дефолт |
| `None` вместо числа | `add(None, 5)` — `TypeError` | Добавь проверку или используй type hints + mypy |
| Пустой `*args` | `sum_all()` — возвращает `0` из `sum([])` | Ожидаемо, но стоит документировать |
| Порядок аргументов | `def f(*args, **kwargs)` — нельзя поменять местами | Позиционные → дефолтные → `*args` → keyword-only → `**kwargs` |

---

## Вопрос на собесе

**Q: В чём разница между `*args` и `**kwargs`?**

> `*args` собирает все лишние позиционные аргументы в **кортеж**, `**kwargs` — все лишние именованные аргументы в **словарь**. Используются для создания гибких функций с переменным числом параметров.

**Q: Что такое type hints и обязательны ли они?**

> Type hints — необязательные аннотации типов для параметров и возвращаемых значений. Они не влияют на выполнение кода, но помогают IDE, линтерам (mypy) и коллегам понять, что ожидает функция. В тестовом коде type hints повышают читаемость.
